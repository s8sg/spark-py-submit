A python library that can submit spark job to spark yarn cluster using rest API
* It Currently supports the CDH(5.6.1) and HDP(2.3.2.0-2950,2.4.0.0-169)

The Library is Inspired from: github.com/bernhard-42/spark-yarn-rest-api


The Library is still in early stage and need testing, fixing and documentation
Please see the test cases for more details


Before running the test cases please follow the below steps:
1> Update the test case Resource Manager and Name Node Host
2> Update the Port if required in settings.py
3> In case of HDP check the right version and update the settings.py
4> Make the spark-jar available in hdfs as: http://rma:50070/webhdfs/v1/user/spark/share/lib/spark-assembly.jar
