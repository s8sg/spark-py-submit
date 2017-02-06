from spark_job_handler import SparkJobHandler
import unittest
import logging

''' Test case to test SparkJobHandler '''
class SparkJobHandlerTest(unittest.TestCase):

    # Note: spark jar should be preset as: 
    #       http://rma:50070/webhdfs/v1/user/spark/share/lib/spark-assembly.jar

    # Note: Jar should be present at : <run_dir>/simple-project/target/scala-2.10/simple-project_2.10-1.0.jar
    def test_local_job_submit(self):
        logger = logging.getLogger('TestLocalJobSubmit')
        sparkJob = SparkJobHandler(logger=logger, job_name="test_local_job_submit", jar="./simple-project/target/scala-2.10/simple-project_2.10-1.0.jar",
                                   run_class="IrisApp", hadoop_rm='rma',
                                   hadoop_web_hdfs='nn', hadoop_nn='nn',
                                   env_type="CDH", local_jar=True, spark_properties=None)
        trackingUrl = sparkJob.run()
        print "Job Tracking URL: %s" % trackingUrl
        
    # NOTE: Jar should be present at: /tmp/test_data/simple-project_2.10-1.0.jar is available at: 
    #       http://rma:50070/webhdfs/v1/tmp/test_data/simple-project_2.10-1.0.jar
    def test_remote_job_submit(self):
        logger = logging.getLogger('TestRemoteJobSubmit')
        sparkJob = SparkJobHandler(logger=logger, job_name="test_remote_job_submit", jar="/tmp/test_data/simple-project_2.10-1.0.jar",
                                   run_class="IrisApp", hadoop_rm='rma',
                                   hadoop_web_hdfs='nn', hadoop_nn='nn',
                                   env_type="CDH", local_jar=False, spark_properties=None)
        trackingUrl = sparkJob.run()
        print "Job Tracking URL: %s" % trackingUrl
        
    def test_spark_properties(self):
        logger = logging.getLogger('TestSparkProperties')
        spark_properties = {
            "spark.executor.memory" : "1G",
            "spark.executor.cores" : "1",
        }
        sparkJob = SparkJobHandler(logger=logger, job_name="test_spark_properties", jar="./simple-project/target/scala-2.10/simple-project_2.10-1.0.jar",
                                   run_class="IrisApp", hadoop_rm='rma',
                                   hadoop_web_hdfs='nn', hadoop_nn='nn',
                                   env_type="CDH", local_jar=True, spark_properties=spark_properties)
        trackingUrl = sparkJob.run()
        print "Job Tracking URL: %s" % trackingUrl


if __name__ == '__main__':
    unittest.main()
