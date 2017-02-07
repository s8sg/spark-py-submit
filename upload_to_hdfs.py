# upload_to_hdfs:
# Tool to upload a local file to a HDFS file system 
import os
import sys
import requests


class UploadToHdfs( object ):
    
    def __init__(self, hadoop_web_hdfs):
        self.hadoop_web_hdfs = "http://%s:50070/webhdfs/v1" % hadoop_web_hdfs

    def _webhdfsGetRequest(self, path, op, allow_redirects=False):
        url = os.path.join(self.hadoop_web_hdfs, path.strip("/"))
        response = requests.get("%s?op=%s" % (url, op), allow_redirects=allow_redirects, verify=False)
        return response.json()

    def _webhdfsPutRequest(self, path, op, allow_redirects=False):
        url = os.path.join(self.hadoop_web_hdfs, path.strip("/"))
        print url
        response = requests.put("%s?op=%s" % (url, op), "", allow_redirects=allow_redirects, verify=False)
        return response
    
    def pathExists(self, path):
        response = self._webhdfsGetRequest(path, "GETFILESTATUS")
        return (response.has_key("FileStatus"), response)

    def uploadFile(self, data, remoteFile, overwrite="true"):
        response = self._webhdfsPutRequest(remoteFile, "CREATE&overwrite=%s" % overwrite)
        location = response.headers.get("Location")
        print location
        if location:
            response = requests.put(location, data, verify=False)
            return (True, response.text)
        return(False, "")

def print_usage(name="upload_to_hdfs.py"):
    usage = "usage: %s <name_node> <local_file_path> <hdfs_file_path>" % name
    print(usage)   

# __main__
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print_usage(sys.argv[0])
        exit(0)
    web_hdfs_addr = sys.argv[1]
    localFile = sys.argv[2]
    remoteFileLocation = sys.argv[3]
    print "Loading data from local file: %s" % localFile
    fd = open(localFile, "rb")    
    hdfsUpload = UploadToHdfs(web_hdfs_addr)
    print "Uploading to: hdfs:%s" % remoteFileLocation
    ret = hdfsUpload.uploadFile(fd, remoteFileLocation)
    if not ret[0]:
        print "Failed to upload File: %s" % ret[1]
        exit(1)
    print "Verifying Upload..."
    ret = hdfsUpload.pathExists(remoteFileLocation)
    if not ret[0]:
        print "File verification failed: %s" % str(ret[1])
        exit(1) 
    print "File successfully uploaded at: hdfs:%s" % remoteFileLocation
