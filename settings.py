# Hadoop Configuration 
HADOOP_RESOURCE_MANAGER_PATH = "http://%s:8088/ws/v1"
HADOOP_WEB_HDFS_PATH = "http://%s:50070/webhdfs/v1"
HADOOP_NAME_NODE_PATH = "%s:8020"

HADOOP_URI_AUTH = False
HADOOP_URI_UNAME = ""
HADOOP_URI_PASS = ""
HADOOP_MAX_JOB_SUBMIT_ATTEMPT = 2
HADOOP_APP_MASTER_MEMORY = 1024
HADOOP_APP_MASTER_CORE = 1

HDFS_ACCESS_UNAME = "hdfs"

SPARK_JAR_LOCATION = {  
        "CDH" :  {
            "common" :  "/user/spark/share/lib/spark-assembly.jar"
        },
        "HDP" : {
            "common" : "/user/spark/share/lib/spark-assembly.jar",
            "2.4.0.0-169" : "/hdp/apps/2.4.0.0-169/spark/spark-hdp-assembly.jar",
            "2.3.2.0-2950" : "/hdp/apps/2.4.0.0-2950/spark/spark-hdp-assembly.jar"
        }
}

SPARK_PROJECT_FOLDER = "/tmp/spark_job"
SPARK_PROPERTY_FILE_NAME = "spark-yarn.properties"
SPARK_DEFAULT_PROPERTIES = {
        "spark.yarn.submit.file.replication" : "3",
        "spark.yarn.executor.memoryOverhead" : "384",
        "spark.yarn.driver.memoryOverhead" : "384",
        "spark.master" : "yarn",
        "spark.submit.deployMode" : "cluster",
        "spark.eventLog.enabled" : "true",
        "spark.yarn.scheduler.heartbeat.interval-ms" : "5000",
        "spark.yarn.preserve.staging.files" : "true",
        "spark.yarn.queue" : "default",
        "spark.yarn.containerLauncherMaxThreads": "25",
        "spark.yarn.max.executor.failures" : "3",
        "spark.executor.instances" : "2",
        "spark.eventLog.dir" : "hdfs\:///spark-history",
        "spark.history.kerberos.enabled" : "true",
        "spark.history.provider" : "org.apache.spark.deploy.history.FsHistoryProvider",
        "spark.history.ui.port" : "18080",
        "spark.history.fs.logDirectory" : "hdfs\:///spark-history",
        "spark.executor.memory" : "2G",
        "spark.executor.cores" : "2",
        "spark.history.kerberos.keytab" : "none",
        "spark.history.kerberos.principal": "none"
}
CDH_VERSION = "CDH-5.6.1-1.cdh5.6.1.p0.3"
HDP_VERSION = "2.4.0.0-169"
SPARK_CDH_EXECUTION_COMMAND = "{{JAVA_HOME}}/bin/java -server -XX:OnOutOfMemoryError='kill %%p' -Xmx1024m -Xms1024m " + \
                                 "-Djava.io.tmpdir={{PWD}}/tmp " + \
                                 "-Dspark.authenticate=false " + \
                                 "-Dspark.shuffle.service.port=7337 " + \
                                 "-Dspark.yarn.keytab" + \
                                 "-Dspark.yarn.app.container.log.dir=<LOG_DIR> " + \
                                 "-Dspark.app.name=%s " + \
                                 "org.apache.spark.deploy.yarn.ApplicationMaster " + \
                                 "--class %s --jar __app__.jar " + \
                                 "--arg '--class' --arg '%s' " + \
                                 "1><LOG_DIR>/AppMaster.stdout " + \
                                 "2><LOG_DIR>/AppMaster.stderr"
SPARK_HDP_EXECUTION_COMMAND =   "{{JAVA_HOME}}/bin/java -server -Xmx1024m " + \
                                "-Dhdp.version=%s " % (HDP_VERSION) + \
                                "-Dspark.yarn.app.container.log.dir=/hadoop/yarn/log/rest-api " + \
                                "-Dspark.app.name=%s " + \
                                "org.apache.spark.deploy.yarn.ApplicationMaster " + \
                                "--class %s --jar __app__.jar " + \
                                "--arg '--class' --arg '%s' " + \
                                "1><LOG_DIR>/AppMaster.stdout " + \
                                "2><LOG_DIR>/AppMaster.stderr"
lzoJar = { 
    "2.3.2.0-2950": "",
    "2.4.0.0-169": "/usr/hdp/2.4.0.0-169/hadoop/lib/hadoop-lzo-0.6.0.2.4.0.0-169.jar"
}

SPARK_HDP_JOB_CLASSPATH = "{{PWD}}<CPS>__spark__.jar<CPS>" + \
                   "{{PWD}}/__app__.jar<CPS>" + \
                   "{{PWD}}/__app__.properties<CPS>" + \
                   "{{HADOOP_CONF_DIR}}<CPS>" + \
                   "/usr/hdp/current/hadoop-client/*<CPS>" + \
                   "/usr/hdp/current/hadoop-client/lib/*<CPS>" + \
                   "/usr/hdp/current/hadoop-hdfs-client/*<CPS>" + \
                   "/usr/hdp/current/hadoop-hdfs-client/lib/*<CPS>" + \
                   "/usr/hdp/current/hadoop-yarn-client/*<CPS>" + \
                   "/usr/hdp/current/hadoop-yarn-client/lib/*<CPS>" + \
                   "{{PWD}}/mr-framework/hadoop/share/hadoop/common/*<CPS>" + \
                   "{{PWD}}/mr-framework/hadoop/share/hadoop/common/lib/*<CPS>" + \
                   "{{PWD}}/mr-framework/hadoop/share/hadoop/yarn/*<CPS>" + \
                   "{{PWD}}/mr-framework/hadoop/share/hadoop/yarn/lib/*<CPS>" + \
                   "{{PWD}}/mr-framework/hadoop/share/hadoop/hdfs/*<CPS>" + \
                   "{{PWD}}/mr-framework/hadoop/share/hadoop/hdfs/lib/*<CPS>" + \
                   "{{PWD}}/mr-framework/hadoop/share/hadoop/tools/lib/*<CPS>" + \
                   "%s<CPS>" % lzoJar[HDP_VERSION] + \
                   "/etc/hadoop/conf/secure<CPS>"

SPARK_CDH_JOB_CLASSPATH = "{{PWD}}<CPS>{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/lib/spark/lib/spark-assembly.jar<CPS>" + \
                   "$HADOOP_CLIENT_CONF_DIR<CPS>$HADOOP_CONF_DIR<CPS>$HADOOP_COMMON_HOME/*<CPS>$HADOOP_COMMON_HOME/lib/*<CPS>" + \
                   "$HADOOP_HDFS_HOME/*<CPS>$HADOOP_HDFS_HOME/lib/*<CPS>$HADOOP_YARN_HOME/*<CPS>$HADOOP_YARN_HOME/lib/*<CPS>" + \
                   "$HADOOP_MAPRED_HOME/*<CPS>$HADOOP_MAPRED_HOME/lib/*<CPS>$MR2_CLASSPATH<CPS>" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/ST4-4.0.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/accumulo-core-1.6.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/accumulo-fate-1.6.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/accumulo-start-1.6.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/accumulo-trace-1.6.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/activation-1.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/ant-1.9.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/ant-launcher-1.9.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/antlr-2.7.7.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/antlr-runtime-3.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/aopalliance-1.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/apache-log4j-extras-1.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/apache-log4j-extras-1.2.17.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/apacheds-i18n-2.0.0-M15.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/apacheds-kerberos-codec-2.0.0-M15.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/api-asn1-api-1.0.0-M20.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/api-util-1.0.0-M20.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/asm-3.2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/asm-commons-3.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/asm-tree-3.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/async-1.4.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/asynchbase-1.5.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/avro-1.7.6-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/avro-compiler-1.7.6-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/avro-ipc-1.7.6-cdh5.6.1-tests.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/avro-ipc-1.7.6-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/avro-mapred-1.7.6-cdh5.6.1-hadoop2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/avro-maven-plugin-1.7.6-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/avro-protobuf-1.7.6-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/avro-service-archetype-1.7.6-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/avro-thrift-1.7.6-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/aws-java-sdk-core-1.10.6.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/aws-java-sdk-kms-1.10.6.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/aws-java-sdk-s3-1.10.6.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/bonecp-0.8.0.RELEASE.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/calcite-avatica-1.0.0-incubating.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/calcite-core-1.0.0-incubating.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/calcite-linq4j-1.0.0-incubating.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-beanutils-1.7.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-beanutils-core-1.8.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-cli-1.2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-codec-1.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-codec-1.8.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-collections-3.2.2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-compiler-2.7.6.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-compress-1.4.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-configuration-1.6.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-daemon-1.0.13.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-dbcp-1.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-digester-1.8.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-el-1.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-httpclient-3.0.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-httpclient-3.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-io-2.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-jexl-2.1.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-lang-2.6.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-logging-1.1.3.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-math-2.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-math3-3.1.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-net-3.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-pool-1.5.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/commons-vfs2-2.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/curator-client-2.6.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/curator-client-2.7.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/curator-framework-2.6.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/curator-framework-2.7.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/curator-recipes-2.6.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/curator-recipes-2.7.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/datanucleus-api-jdo-3.2.6.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/datanucleus-core-3.2.10.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/datanucleus-rdbms-3.2.9.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/derby-10.11.1.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/eigenbase-properties-1.1.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/fastutil-6.3.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-avro-source-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-dataset-sink-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-file-channel-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-hdfs-sink-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-hive-sink-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-irc-sink-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-jdbc-channel-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-jms-source-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-kafka-channel-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-kafka-source-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-ng-auth-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-ng-elasticsearch-sink-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-ng-embedded-agent-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-ng-hbase-sink-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-ng-kafka-sink-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-ng-log4jappender-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-ng-morphline-solr-sink-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-ng-node-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-scribe-source-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-spillable-memory-channel-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-taildir-source-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-thrift-source-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-tools-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/flume-twitter-source-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/geronimo-annotation_1.0_spec-1.1.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/geronimo-jaspic_1.0_spec-1.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/geronimo-jta_1.1_spec-1.1.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/groovy-all-2.4.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/gson-2.2.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/guava-11.0.2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/guava-11.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/guava-14.0.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/guice-3.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/guice-servlet-3.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-annotations-2.6.0-cdh5.6.1.jar: " + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-ant-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-archive-logs-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-archives-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-auth-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-aws-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-azure-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-common-2.6.0-cdh5.6.1-tests.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-common-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-datajoin-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-distcp-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-extras-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-gridmix-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-hdfs-2.6.0-cdh5.6.1-tests.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-hdfs-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-hdfs-nfs-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-mapreduce-client-app-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-mapreduce-client-common-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-mapreduce-client-core-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-mapreduce-client-hs-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-mapreduce-client-hs-plugins-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-mapreduce-client-jobclient-2.6.0-cdh5.6.1-tests.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-mapreduce-client-jobclient-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-mapreduce-client-nativetask-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-mapreduce-client-shuffle-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-mapreduce-examples-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-nfs-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-openstack-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-rumen-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-sls-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-streaming-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-yarn-api-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-yarn-applications-distributedshell-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-yarn-applications-unmanaged-am-launcher-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-yarn-client-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-yarn-common-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-yarn-registry-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-yarn-server-applicationhistoryservice-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-yarn-server-common-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-yarn-server-nodemanager-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-yarn-server-resourcemanager-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-yarn-server-tests-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hadoop-yarn-server-web-proxy-2.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hamcrest-core-1.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hamcrest-core-1.3.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hbase-client-1.0.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hbase-common-1.0.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hbase-hadoop-compat-1.0.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hbase-hadoop2-compat-1.0.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hbase-protocol-1.0.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hbase-server-1.0.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/high-scale-lib-1.1.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-accumulo-handler-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-ant-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-beeline-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-cli-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-common-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-contrib-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-exec-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-hbase-handler-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-hwi-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-jdbc-1.1.0-cdh5.6.1-standalone.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-jdbc-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-metastore-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-serde-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-service-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-shims-0.23-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-shims-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-shims-common-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-shims-scheduler-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hive-testutils-1.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/htrace-core-3.2.0-incubating.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/htrace-core4-4.0.1-incubating.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/httpclient-4.2.5.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/httpcore-4.2.5.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/hue-plugins-3.9.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/irclib-1.10.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jackson-annotations-2.2.3.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jackson-core-2.2.3.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jackson-core-asl-1.8.8.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jackson-databind-2.2.3.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jackson-jaxrs-1.8.8.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jackson-mapper-asl-1.8.8.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jackson-xc-1.8.8.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/janino-2.7.6.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jasper-compiler-5.5.23.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jasper-runtime-5.5.23.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/java-xmlbuilder-0.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/javax.inject-1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jaxb-api-2.2.2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jaxb-impl-2.2.3-1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jcommander-1.32.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jdo-api-3.0.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jersey-client-1.9.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jersey-core-1.9.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jersey-guice-1.9.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jersey-json-1.9.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jersey-server-1.9.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jets3t-0.9.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jettison-1.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jetty-6.1.26.cloudera.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jetty-all-7.6.0.v20120127.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jetty-all-server-7.6.0.v20120127.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jetty-util-6.1.26.cloudera.2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jetty-util-6.1.26.cloudera.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jline-2.11.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jline-2.12.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/joda-time-2.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jopt-simple-3.2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jpam-1.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jsch-0.1.42.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jsp-api-2.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jsr305-1.3.9.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jsr305-3.0.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/jta-1.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/junit-4.11.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/kafka_2.10-0.8.1.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/kite-data-core-1.0.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/kite-data-hbase-1.0.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/kite-data-hive-1.0.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/kite-hadoop-compatibility-1.0.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/leveldbjni-all-1.8.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/libfb303-0.9.2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/libthrift-0.9.2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/log4j-1.2.16.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/log4j-1.2.17.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/logredactor-1.0.3.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/mail-1.4.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/mapdb-0.9.9.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/maven-scm-api-1.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/maven-scm-provider-svn-commons-1.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/maven-scm-provider-svnexe-1.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/metrics-core-2.2.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/metrics-core-3.0.2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/metrics-json-3.0.2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/metrics-jvm-3.0.2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/microsoft-windowsazure-storage-sdk-0.6.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/mina-core-2.0.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/mockito-all-1.8.5.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/netty-3.6.2.Final.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/netty-all-4.0.23.Final.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/opencsv-2.3.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/oro-2.0.8.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/paranamer-2.3.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-avro-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-cascading-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-column-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-common-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-encoding-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-format-2.1.0-cdh5.6.1-javadoc.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-format-2.1.0-cdh5.6.1-sources.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-format-2.1.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-generator-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-hadoop-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-hadoop-bundle-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-jackson-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-pig-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-pig-bundle-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-protobuf-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-scala_2.10-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-scrooge_2.10-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-test-hadoop2-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-thrift-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/parquet-tools-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/pentaho-aggdesigner-algorithm-5.1.5-jhyde.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/plexus-utils-1.5.6.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/protobuf-java-2.5.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/regexp-1.3.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/scala-library-2.10.4.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/serializer-2.7.2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/servlet-api-2.5-20110124.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/servlet-api-2.5.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/slf4j-api-1.7.5.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/slf4j-log4j12-1.7.5.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/snappy-java-1.0.4.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/spark-1.5.0-cdh5.6.1-yarn-shuffle.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/spark-streaming-flume-sink_2.10-1.5.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/stax-api-1.0-2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/stax-api-1.0.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/stringtemplate-3.2.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/super-csv-2.2.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/tempus-fugit-1.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/trevni-avro-1.7.6-cdh5.6.1-hadoop2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/trevni-avro-1.7.6-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/trevni-core-1.7.6-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/twitter4j-core-3.0.3.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/twitter4j-media-support-3.0.3.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/twitter4j-stream-3.0.3.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/unused-1.0.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/velocity-1.5.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/velocity-1.7.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/xalan-2.7.2.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/xercesImpl-2.9.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/xml-apis-1.3.04.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/xmlenc-0.52.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/xz-1.0.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/zkclient-0.3.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/jars/zookeeper-3.4.5-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/lib/flume-ng/lib/flume-ng-configuration-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/lib/flume-ng/lib/flume-ng-core-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/lib/flume-ng/lib/flume-ng-sdk-1.6.0-cdh5.6.1.jar:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/lib/hadoop/LICENSE.txt:" + \
                   "{{HADOOP_COMMON_HOME}}/../../../"+CDH_VERSION+"/lib/hadoop/NOTICE.txt"
