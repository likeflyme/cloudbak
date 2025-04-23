# import binascii
#
# from app.models.hard_link_image import HardLinkImageAttribute
# from db.wx_db import get_session_local
#
#
# hardlink_image_path = 'D:\\workspace\\sessions\\8\\wxid_b125nd5rc59r12\\Msg\\decoded_HardLinkImage.db'
#
# file_md5 = 'f73415678937715f9ebc988768879089'
# md5_blob = binascii.unhexlify(file_md5)
#
# session_local = get_session_local(hardlink_image_path)
#
# db = session_local()
# try:
#     img = db.query(HardLinkImageAttribute).filter_by(MD5=md5_blob).first()
#     print(img)
# finally:
#     db.close()

import sqlite3
import binascii


hardlink_image_path = 'D:\\workspace\\sessions\\8\\wxid_b125nd5rc59r12\\Msg\\decoded_HardLinkImage.db'

conn = sqlite3.connect(hardlink_image_path)
c = conn.cursor()
print("数据库打开成功")

md5 = '97b3f38e0a03e078e8860d7c00e941e7'
md5_blob = binascii.unhexlify(md5)

cursor = c.execute("""
    SELECT
        Md5Hash,
        MD5,
        FileName,
        HardLinkImageID.Dir AS dirName1,
        HardLinkImageID2.Dir AS dirName2 
    FROM
        HardLinkImageAttribute
        JOIN HardLinkImageID ON HardLinkImageAttribute.DirID1 = HardLinkImageID.DirID
        JOIN HardLinkImageID AS HardLinkImageID2 ON HardLinkImageAttribute.DirID2 = HardLinkImageID2.DirID 
    WHERE
        MD5 = ?;
""", (md5_blob, ))

for row in cursor:
    print(row)
    print('FileStorage/MsgAttach/' + row[3] + '/Image/' + row[4] + '/' + row[2])

conn.close()
