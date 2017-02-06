import settings
import ntpath
import requests
import json
import os
import os.path

''' This is the implemenattion of a spark Job Handler '''
class SparkJobHandler( object ):

    # SparkJobHandlerImpl
    # logger : The logger object
    # job_name : the name of the job
    # jar : the remote jar path
    # run_class : the entry point of the spark job
    # hadoop_rm : the ip address of the hadoop rm
    # hadoop_web_hdfs : the ip address of the hdfs web api
    # hadoop_nn : the ip address of the hadoop name node
    # env_type: The Spark Running ENV type (CDH or HDP)
    # local_jar : Id the jar path provided is local  
    # spark_properties : spark properties values
    def __init__(self, logger, job_name, jar, run_class, hadoop_rm, 
            hadoop_web_hdfs, hadoop_nn, env_type="CDH" ,local_jar=False, spark_properties=None):
        self.logger = logger
        self.job_name = job_name
        self.spark_project_folder = settings.SPARK_PROJECT_FOLDER
        self.jar = jar
        self.run_class = run_class
        self.hadoop_rm = settings.HADOOP_RESOURCE_MANAGER_PATH % hadoop_rm
        self.hadoop_web_hdfs = settings.HADOOP_WEB_HDFS_PATH % hadoop_web_hdfs
        self.hadoop_nn = settings.HADOOP_NAME_NODE_PATH % hadoop_nn
        self.hadoop_uri_auth = settings.HADOOP_URI_AUTH
        self.hadoop_uri_uname = settings.HADOOP_URI_UNAME
        self.hadoop_uri_pass = settings.HADOOP_URI_PASS
        self.hdfs_access_uname = settings.HDFS_ACCESS_UNAME
        self.spark_properties = settings.SPARK_DEFAULT_PROPERTIES
        self.spark_properties_name = settings.SPARK_PROPERTY_FILE_NAME
        self.spark_jar_path = settings.SPARK_JAR_LOCATION[env_type]["common"]
        self.local_jar = local_jar
        self.env_type = env_type
        if spark_properties is not None:
            for key in spark_properties:
                self.spark_properties[key] = spark_properties[key]

    def _createHdfsPath(self, path):
        return os.path.join("hdfs://", self.hadoop_nn, path.strip("/"))

    def _webhdfsGetRequest(self, path, op, allow_redirects=False):
        url = os.path.join(self.hadoop_web_hdfs, path.strip("/"))
        response = requests.get("%s?op=%s" % (url, op), allow_redirects=allow_redirects, verify=self.hadoop_uri_auth, auth=(self.hadoop_uri_uname, self.hadoop_uri_pass))
        return response.json()

    def _webhdfsPutRequest(self, path, op, allow_redirects=False):
        url = os.path.join(self.hadoop_web_hdfs, path.strip("/"))
        response = requests.put("%s?op=%s" % (url, op), "", allow_redirects=allow_redirects, verify=self.hadoop_uri_auth, auth=(self.hadoop_uri_uname, self.hadoop_uri_pass))
        return response
    
    def _pathExists(self, path):
        response = self._webhdfsGetRequest(path, "GETFILESTATUS")
        return (response.has_key("FileStatus"), response)

    def _createDir(self, path):
        response = self._webhdfsPutRequest(path, "MKDIRS").json()
        return (response.has_key("boolean") and response["boolean"], response)

    def _uploadFile(self, data, remoteFile, overwrite="true"):
        response = self._webhdfsPutRequest(remoteFile, "CREATE&overwrite=%s" % overwrite)
        location = response.headers.get("Location")
        if location:
            response = requests.put(location, data, verify=self.hadoop_uri_auth, auth=(self.hadoop_uri_uname, self.hadoop_uri_pass))
            return (True, response.text)
        return(False, "")

    def _createCacheValue(self, path, size, timestamp):
        return {
            "resource": self._createHdfsPath(path),
            "type": "FILE",
            "visibility": "APPLICATION",
            "size": size,
            "timestamp": timestamp
        }

    def _createNewApplication(self):
        url = os.path.join(self.hadoop_rm, "cluster/apps/new-application")
        response = requests.post(url, "", verify=self.hadoop_uri_auth, auth=(self.hadoop_uri_uname, self.hadoop_uri_pass))
        return (True, response.json())

    def _submitSparkJob(self, sparkJson):
        url = os.path.join(self.hadoop_rm, "cluster/apps")
        response = requests.post(url, sparkJson, headers={"Content-Type": "application/json"}, verify=self.hadoop_uri_auth, auth=(self.hadoop_uri_uname, self.hadoop_uri_pass))
        return response

    def _getFileName(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    # Method to run the SparkJob
    def run(self):
        # Check if the remote spark assembly exists
        ret = self._pathExists(self.spark_jar_path)
        if not ret[0]: raise Exception("Spark jar (spark_assembly.jar) not found: " + ret[1])
        sparkJarFileStatus = ret[1]["FileStatus"]
        # Check if the project folder is created
        if not self._pathExists(self.spark_project_folder):
            ret = self._createDir(self.spark_project_folder)
            if not ret[0]: raise Exception("Falied to create exception: " + json.dumps(ret[1]))
        appJarFileStatus = None
        remoteJarLocation = self.jar
        # In case of local jar copy the jar to the hdfs
        if self.local_jar:
            # Local jar gets copied in a project specific location
            remoteJarLocation = os.path.join(self.spark_project_folder, self.job_name, self._getFileName(self.jar))
            # Open the lcoal file TODO: handle Exception
            fd = open(self.jar, "rb")
            ret = self._uploadFile(fd, remoteJarLocation)
            if not ret[0]: raise Exception("Falied to upload local jar file: " + str(ret[1]))
            ret = self._pathExists(remoteJarLocation)
            appJarFileStatus = ret[1]["FileStatus"]
        else:
            # check if the jar is present in the HDFS
            ret = self._pathExists(remoteJarLocation)
            if not ret[0]: raise Exception("HDFS path doesn't exist: " + str(ret[1]))
            appJarFileStatus = ret[1]["FileStatus"]
        # Create and upload spark properties
        spark_properties_data = ""
        for key in self.spark_properties:
            spark_properties_data = spark_properties_data + "\n" + key + "=" + self.spark_properties[key]
        remoteSparkProperties = os.path.join(self.spark_project_folder, self.job_name, self.spark_properties_name)
        ret = self._uploadFile(spark_properties_data, remoteSparkProperties)
        if not ret[0]: raise Exception("Falied to upload local spark properties file: " + str(ret[1]))
        ret = self._pathExists(remoteSparkProperties)
        sparkPropertiesFileStatus = ret[1]["FileStatus"]
        # Create new Hadoop application for spark
        yarnApp = self._createNewApplication()
        if not yarnApp[0]: raise Exception("Failed to create a new application to Hadoop resource manager: " + str(ret[1]))

        commands = {}
        environment = {}
        application_type = {} 
        # Define spark Job based on env_typr
        if self.env_type == 'CDH':
            command = {
                    "command" : settings.SPARK_CDH_EXECUTION_COMMAND % (self.job_name, self.run_class, self.job_name)
                }
            application_type = "SPARK"
            environment = {
                    "entry":
                    [
                        {
                            "key": "SPARK_USER",
                            "value": "%s" % settings.HDFS_ACCESS_UNAME
                        },
                        {
                            "key": "HADOOP_USER_NAME",
                            "value": "%s" % settings.HDFS_ACCESS_UNAME
                        },
                        {
                            "key": "SPARK_YARN_STAGING_DIR",
                            "value": ".sparkStaging/%s" % self.job_name 
                        },
                        {
                            "key": "SPARK_YARN_MODE",
                            "value": True
                        },
                        {
                            "key": "user.name",
                            "value": "%s" % settings.HDFS_ACCESS_UNAME
                        },
                        {
                            "key": "CLASSPATH",
                            "value": settings.SPARK_CDH_JOB_CLASSPATH                         
                        },
                        {
                            "key": "SPARK_YARN_CACHE_FILES",
                            "value": "%s#__app__.jar,%s#__spark__.jar" % (self._createHdfsPath(remoteJarLocation), self._createHdfsPath(self.spark_jar_path))
                        },
                        {
                            "key": "SPARK_YARN_CACHE_FILES_FILE_SIZES",
                            "value": "%d,%d" % (appJarFileStatus["length"], sparkJarFileStatus["length"])
                        },
                        {
                            "key": "SPARK_YARN_CACHE_FILES_TIME_STAMPS",
                            "value": "%d,%d" % (appJarFileStatus["modificationTime"], sparkJarFileStatus["modificationTime"])
                        },
                        {
                            "key": "SPARK_YARN_CACHE_FILES_VISIBILITIES",
                            "value": "PUBLIC,PRIVATE"
                        },
                        {
                            "key": "LD_LIBRARY_PATH",
                            "value": "{{HADOOP_COMMON_HOME}}/../../../" + settings.CDH_VERSION + "/lib/hadoop/lib/native:$LD_LIBRARY_PATH"
                        }
                    ]
                }
        elif self.env_type == 'HDP':
            command = {
                    "command" : settings.SPARK_HDP_EXECUTION_COMMAND % (settings.HDP_VERSION, self.job_name, self.run_class, self.job_name)
                }
            application_type = "YARN"
            environment = {
                    "entry":
                    [
                        {
                            "key": "HADOOP_USER_NAME",
                            "value": "%s" % settings.HDFS_ACCESS_UNAME
                        },
                        {
                            "key": "HDP_VERSION",
                            "value": "%s" % settings.HDP_VERSION
                        },
                        {
                            "key": "SPARK_YARN_MODE",
                            "value": True
                        },
                        {
                            "key": "user.name",
                            "value": "%s" % settings.HDFS_ACCESS_UNAME
                        },
                        {
                            "key": "CLASSPATH",
                            "value": settings.SPARK_HDP_JOB_CLASSPATH                         
                        },
                        {
                            "key": "SPARK_YARN_CACHE_FILES",
                            "value": "%s#__app__.jar,%s#__spark__.jar" % (self._createHdfsPath(remoteJarLocation), self._createHdfsPath(self.spark_jar_path))
                        },
                        {
                            "key": "SPARK_YARN_CACHE_FILES_FILE_SIZES",
                            "value": "%d,%d" % (appJarFileStatus["length"], sparkJarFileStatus["length"])
                        },
                        {
                            "key": "SPARK_YARN_CACHE_FILES_TIME_STAMPS",
                            "value": "%d,%d" % (appJarFileStatus["modificationTime"], sparkJarFileStatus["modificationTime"])
                        },
                        {
                            "key": "SPARK_YARN_CACHE_FILES_VISIBILITIES",
                            "value": "PUBLIC,PRIVATE"
                        }
                    ]
                }

        else:
            raise Exception("Falied to run job: Invalid env_type: " + self.env_type)

        # Create spark Job definition
        sparkJob = {
            "application-id": yarnApp[1]["application-id"],
            "application-name": self.job_name,
            "am-container-spec": {
                "local-resources": {
                    "entry":[
                        {
                            "key": "__spark__.jar",
                            "value": self._createCacheValue(self.spark_jar_path, sparkJarFileStatus["length"], sparkJarFileStatus["modificationTime"])
                        },
                        {
                            "key": "__app__.jar",
                            "value": self._createCacheValue(remoteJarLocation, appJarFileStatus["length"], appJarFileStatus["modificationTime"])
                        },
                        {
                            "key": "__app__.properties",
                            "value": self._createCacheValue(remoteSparkProperties, sparkPropertiesFileStatus["length"], sparkPropertiesFileStatus["modificationTime"])
                        }
                    ]
                },
                "commands": command,
                "environment":  environment            
            },
            "unmanaged-AM": False,
            "max-app-attempts": settings.HADOOP_MAX_JOB_SUBMIT_ATTEMPT,
            "resource": {  
                "memory": settings.HADOOP_APP_MASTER_MEMORY,
                "vCores": settings.HADOOP_APP_MASTER_CORE
            },
            "application-type": application_type,
            "keep-containers-across-application-attempts": False
        }
        # Submit the spark Job
        sparkJobJson = json.dumps(sparkJob, indent=2, sort_keys=True)
        response = self._submitSparkJob(sparkJobJson)
        trackingUrl = response.headers["Location"].replace("apps//", "apps/")
        return trackingUrl
