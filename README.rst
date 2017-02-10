Spark Py Submit
===============

A python library that can submit spark job to spark cluster and standalone using
rest API

| **Note: It Currently supports the CDH(5.6.1) and
  HDP(2.3.2.0-2950,2.4.0.0-169) yarn cluster**
| The Library is Inspired from:
  ``github.com/bernhard-42/spark-yarn-rest-api``

Getting Started:
~~~~~~~~~~~~~~~~

Use the library
^^^^^^^^^^^^^^^

.. code:: python

    # Import the SparkJobHandler
    from spark_job_handler import SparkJobHandler

    ...

    logger = logging.getLogger('TestLocalJobSubmit')
    # Create a spark JOB
    # jobName:           name of the Spark Job   
    # jar:               location of the Jar (local/hdfs)  
    # run_class:         entry class of the appliaction   
    # hadoop_rm:         hadoop resource manager host ip  
    # hadoop_web_hdfs:   hadoop web hdfs ip   
    # hadoop_nn:         hadoop name node ip (Normally same as of web_hdfs)  
    # env_type:          env type is CDH or HDP  
    # local_jar:         flag to define if a jar is local (Local jar gets uploaded to hdfs)  
    # spark_properties:  custom properties that need to be set 
    sparkJob = SparkJobHandler(logger=logger, job_name="test_local_job_submit", 
                jar="./simple-project/target/scala-2.10/simple-project_2.10-1.0.jar",
                run_class="IrisApp", hadoop_rm='rma', hadoop_web_hdfs='nn', hadoop_nn='nn',
                env_type="CDH", local_jar=True, spark_properties=None)
    trackingUrl = sparkJob.run()
    print "Job Tracking URL: %s" % trackingUrl

| The above code starts an spark application using the local jar
  (simple-project/target/scala-2.10/simple-project\_2.10-1.0.jar)
| For more example see the
  `test\_spark\_job\_handler.py <https://github.com/s8sg/spark-py-submit/blob/master/test_spark_job_handler.py>`__

Build the simple-project
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

      $ cd simple-project
      $ sbt package;cd ..

The above steps will create the target jar as:
``./simple-project/target/scala-2.10/simple-project_2.10-1.0.jar``

Update the nodes Ip in test:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Add the node IP for hadoop resource manager and Name node in the
  test\_cases:
| \* rm: Resource Manager \* nn: Name Node

load the data and make it available to HDFS:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

      $ wget https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data

upload data to the HDFS:

.. code:: bash

      $ python upload_to_hdfs.py <name_nodei_ip> iris.data /tmp/iris.data

Run the test cases:
^^^^^^^^^^^^^^^^^^^

Make the simple-project jar available in HDFS to test remote jar:

.. code:: bash

      $ python upload_to_hdfs.py <name_nodei_ip> simple-project/target/scala-2.10/simple-project_2.10-1.0.jar /tmp/test_data/simple-project_2.10-1.0.jar

Run the test:

.. code:: bash

      $ python test_spark_job_handler.py 

Utility:
~~~~~~~~

-  upload\_to\_hdfs.py: upload local file to hdfs file system

Notes:
~~~~~~

| The Library is still in early stage and need testing, bug-fixing and
  documentation
| Before running, follow the below steps:
| \* Update the ResourceManager,NameNode and WebHDFS Port if required in
  settings.py
| \* Make the spark-jar available in hdfs as:
  ``hdfs:/user/spark/share/lib/spark-assembly.jar``
| For Contribution Please Create Issue corresponding PR at: github.com/s8sg/spark-py-submit
