# Spark Py Submit #

A python library that can submit spark job to spark yarn cluster using rest API   

**Note: It Currently supports the CDH(5.6.1) and HDP(2.3.2.0-2950,2.4.0.0-169)**   
     **The Library is Inspired from: `github.com/bernhard-42/spark-yarn-rest-api`**


#### Getting Started:
##### Use the library
```
	# Import the SparkJobHandler
	from spark_job_handler import SparkJobHandler

	...

	logger = logging.getLogger('TestLocalJobSubmit')
	# Create a spark JOB
	sparkJob = SparkJobHandler(logger=logger, job_name="test_local_job_submit", 
					jar="./simple-project/target/scala-2.10/simple-project_2.10-1.0.jar",
					run_class="IrisApp", hadoop_rm='rma', hadoop_web_hdfs='nn', hadoop_nn='nn',
					env_type="CDH", local_jar=True, spark_properties=None)
	trackingUrl = sparkJob.run()
	print "Job Tracking URL: %s" % trackingUrl
```
The above code starts an spark application using the local jar (simple-project/target/scala-2.10/simple-project_2.10-1.0.jar)  
For more example see the [test_spark_job_handler.py](https://github.com/s8sg/spark-py-submit/blob/master/test_spark_job_handler.py)  

**Spark Job Handler** :  
**jobName:** name of the Spark Job  
**jar:** location of the Jar (local/hdfs)  
**run_class:** Entry class of the appliaction  
**hadoop_rm:** hadoop resource manager host ip  
**hadoop_web_hdfs:** hadoop web hdfs ip  
**hadoop_nn:** hadoop name node ip (Normally same as of web_hdfs)  
**env_type:** env type is CDH or HDP  
**local_jar:** flag to define if a jar is local (Local jar gets uploaded to hdfs at submit)  
**spark_properties:** custom properties that need to be set  


##### Utility:
**upload_to_hdfs.py**: upload local file to hdfs file system  

##### Notes: 
The Library is still in early stage and need testing, fixing and documentation   
Before running, follow the below steps:   
* Update the Port if required in `settings.py`  
* Make the spark-jar available in hdfs as: `/user/spark/share/lib/spark-assembly.jar`
