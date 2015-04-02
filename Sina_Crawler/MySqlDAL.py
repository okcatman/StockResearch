# -*- coding: utf8 -*-
import MySQLdb
import sys
from ConnectDB import ConnectDB
from Config import Config
import traceback
from LoggingRecord import LogRec

reload(sys)
sys.setdefaultencoding( "utf-8" )
class MySqlDAL(object):

    def __init__(self,db_no="0"):
        self.db_no = db_no
        db_config = Config.MYSQL[db_no] # 获取配置文件中连接信息
        self.__con = MySQLdb.connect(host=db_config["host"],user=db_config["uname"],passwd=db_config["pwd"],db=db_config["db_name"],port=db_config["port"],charset=db_config["encoding"])
        self.__con.autocommit = True
        self.__encoding=ConnectDB.get_encoding(db_no)

    # 插入一行数据，data_source为字典，其中键为数据表字段,值为要写入数据表相应字段的值，成功返回写入数据的自增长主键
    # data_source={}
    def insert_data(self,data_source,table_name):
        # 在默认情况下cursor方法返回的是BaseCursor类型对象，BaseCursor类型对象在执行查询后每条记录的结果以列表(list)表示。如果要返回字典(dict)表示的记录，就要设置cursorclass参数
        cursor=self.__con.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql="INSERT INTO "+table_name+"("
        key_str=""
        value_str=""
        for key in data_source.keys():
            value=MySQLdb.escape_string(str(data_source[key]))  # 对要插入的数据进行转义，变成数据库对应的字段类型
            key_str=key_str+key+","
            value_str=value_str+"'"+value+"',"
        key_str=key_str[:-1]
        value_str=value_str[:-1]
        sql=sql+key_str+") VALUES ("+value_str+" )"
        try:
            encode_cmd="set names "+self.__encoding
            cursor.execute(encode_cmd)
            result=cursor.execute(sql)
            self.__con.commit()
            cursor.close()
            primary_key=int(cursor.lastrowid) # 最后插入行的主键ID
            if(primary_key):
                return primary_key
            return result
        except:
            self.__dispose_except(sql)



    # data_source 中的每一项必须为元祖  data_keys=[],data_source=[(),()...]
    def insert_many(self,data_keys,data_source,table_name):
        cursor=self.__con.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql="INSERT INTO "+table_name+"("
        key_str=""
        value_str=""
        data_dis=len(data_keys)
        for i in xrange(0,data_dis):
            value_str=value_str+'%s,'
        value_str=value_str[:-1]
        for key in data_keys:
            key_str=key_str+key+","
        key_str=key_str[:-1]
        sql=sql+key_str+") VALUES ("+value_str+")"
        try:
            encode_cmd="set names "+self.__encoding
            cursor.execute(encode_cmd)
            # data_source 中的每一项必须为元祖
            result=cursor.executemany(sql,data_source)
            self.__con.commit()
            cursor.close()
            primary_key=int(cursor.lastrowid)
            if(primary_key):return primary_key
            return result
        except:
            self.__dispose_except(sql)


    # datamanager={}
    def __make_sql(self,table_name,data):
        sql="INSERT INTO "+table_name+"("
        key_str=""
        value_str=""
        for key in data.keys():
            value=(str(data[key]))
            value=MySQLdb.escape_string(value)
            key_str=key_str+key+","
            value_str=value_str+"'"+value+"',"
        key_str=key_str[:-1]
        value_str=value_str[:-1]
        sql=sql+key_str+") VALUES ("+value_str+" )"
        return sql

    # 获得多维多行数据，sql为查询的SELECT的语句，返回的是数组，数据每一项为字典，改字典的键为数据表字段，值为查询值
    def get_dimensions_rows(self,sql):
        try:
            cursor=self.__con.cursor(cursorclass = MySQLdb.cursors.DictCursor)
            cursor.execute(sql)
            result=cursor.fetchall()
            cursor.close()
            return result
        except :
            self.__dispose_except(sql)

    # 获得多维一行数据
    def get_dimensions_one_row(self,sql):
        try:
            cursor=self.__con.cursor(cursorclass = MySQLdb.cursors.DictCursor)
            cursor.execute(sql)
            result= cursor.fetchone()
            cursor.close()
            return result
        except :
            self.__dispose_except(sql)

    # 更新数据表一项，根据goal_key='goal_value'来定位更新的数据行
    #source={}  filter_collection={}
    def update_data(self,source,table_name,filter_collection):
        sql="UPDATE "+table_name+" set "
        update_str=""
        for key in source.keys():
            update_str=update_str+key+"='"+MySQLdb.escape_string(str(source[key]))+"',"
        update_str=update_str[:-1]
        filter_str=""
        for key in filter_collection.keys():
            filter_str=filter_str+str(key)+"='"+str(filter_collection[key])+"' AND "
        str_len=len(filter_str)
        filter_str=filter_str[0:(str_len-4)]
        sql=sql+update_str+" where "+filter_str
        try:
            cursor=self.__con.cursor(cursorclass = MySQLdb.cursors.DictCursor)
            encode_cmd="set names "+self.__encoding
            cursor.execute(encode_cmd)
            result=cursor.execute(sql)
            self.__con.commit()
            cursor.close()
            return result
        except:
            self.__dispose_except(sql)

    # 更新多条数据  data_keys=[] ,data_source=[(修改值1),(2),(3)...(过滤条件1),(2)...] ,filter_collection_key=[key1,key2,...]
    def update_data_many(self,data_keys,data_source,table_name,filter_collection_key):
        cursor=self.__con.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        sql="UPDATE "+table_name+" set "
        update_str = ""
        data_dis=len(data_keys)
        for i in xrange(0,data_dis):
            update_str=update_str+data_keys[i]+'=%s,'
        update_str = update_str[:-1]
        filter_str=""
        for key in filter_collection_key:
            filter_str=filter_str+str(key)+"=%s AND "
        str_len=len(filter_str)
        filter_str=filter_str[0:(str_len-4)]
        sql=sql+update_str+" where "+filter_str
        try:
            encode_cmd="set names "+self.__encoding
            cursor.execute(encode_cmd)
            # data_source 中的每一项必须为元祖
            result=cursor.executemany(sql,data_source)
            self.__con.commit()
            cursor.close()
            return result
        except:
            self.__dispose_except(sql)

    #source={}  filter_collection=[[,],[,]]
    def update_from_conditions(self,source,table_name,filter_collection):
        sql="UPDATE "+table_name+" set "
        update_str=""
        for key in source.keys():
            update_str=update_str+key+"='"+MySQLdb.escape_string(str(source[key]))+"',"
        update_str=update_str[:-1]
        filter_str=""
        for e in filter_collection:
            filter_str=filter_str+str(e[0])+"='"+str(e[1])+"' AND "
        str_len=len(filter_str)
        filter_str=filter_str[0:(str_len-4)]
        sql=sql+update_str+" where "+filter_str
        try:
            cursor=self.__con.cursor(cursorclass = MySQLdb.cursors.DictCursor)
            encode_cmd="set names "+self.__encoding
            cursor.execute(encode_cmd)
            result=cursor.execute(sql)
            self.__con.commit()
            cursor.close()
            return result
        except:
            self.__dispose_except(sql)

    # 根据条件删除数据   {}
    def delete_data(self,table_name,filter_collection,encoding='utf8'):
        filter_str=""
        for key in filter_collection.keys():
            filter_str=filter_str+str(key)+"='"+str(filter_collection[key])+"' AND "
        str_len=len(filter_str)
        filter_str=filter_str[0:(str_len-4)]
        sql="DELETE FROM "+table_name+" WHERE "+filter_str
        try:
            cursor=self.__con.cursor(cursorclass = MySQLdb.cursors.DictCursor)
            sql=unicode(sql,encoding)
            result=cursor.execute(sql)
            self.__con.commit()
            cursor.close()
            return result
        except :
            self.__dispose_except(sql)

    # collection  [[[,],[,]...]
    def delete_from_condition(self,table_name,filter_collection,encoding='utf8'):
        filter_str=""
        for e in filter_collection:
            filter_str=filter_str+str(e[0])+"='"+str(e[1])+"' AND "
        str_len=len(filter_str)
        filter_str=filter_str[0:(str_len-4)]
        sql="DELETE FROM "+table_name+" WHERE "+filter_str
        try:
            cursor=self.__con.cursor(cursorclass = MySQLdb.cursors.DictCursor)
            sql=unicode(sql,encoding)
            result=cursor.execute(sql)
            self.__con.commit()
            cursor.close()
            return result
        except :
            self.__dispose_except(sql)

    # 清除整个表的数据
    def delete_table(self,table_name):
        sql="DELETE FROM "+table_name
        try:
            cursor=self.__con.cursor(cursorclass = MySQLdb.cursors.DictCursor)
            result=cursor.execute(sql)
            self.__con.commit()
            cursor.close()
            return result
        except :
            self.__dispose_except(sql)

    # 分页
    # 获取数据的方法，column_collection为{"id":[9,0,False],"age":[24,1,True]}这种形式
    # "id":[9,0,False]代表 where id=9,0表示等于，false代表or ,一条的话false没有用
    # {"id":[9,0,False],"age":[24,1,True]} 转化为sql: where age>'24' or 'id'='9'，1代表大于，-1代表小于
    # column_collection为查询的列，为空代表全部查询
    # order为字典{"id":1}，表示id正序排列，{"id":-1}，表示结果反序排列
    def get_data(self,table_name,column_collection=None,filter=None,order=None,limit=0,skip=0):
        col_str=""
        if(column_collection):
            for col in column_collection:
                col_str=col_str+col+","
            col_str=col_str[:-1]
        else:
            col_str="*"

        sql="SELECT "+col_str+" FROM "+table_name
        if(filter):
            filter_str=""
            for key in filter.keys():
                if(filter[key][2]):
                    _str="AND "+key+self.__change_filter(filter[key][1])+"'"+str(filter[key][0])+"' "
                else:
                    _str="OR "+key+self.__change_filter(filter[key][1])+"'"+str(filter[key][0])+"' "
                filter_str=filter_str+_str
            filter_array=filter_str.split(" ")
            filter_array=filter_array[1:]
            filter_str=""
            for row in filter_array:
                filter_str=filter_str+row+" "
            sql=sql+" WHERE " +filter_str
        if(order):
            order_str=" ORDER BY "
            for key in order.keys():
                order_str=order_str+key
                if(order[key]==1):
                    order_str=order_str+" ,"
                if(order[key]==-1):
                    order_str=order_str+" desc ,"
            order_str=order_str[:-1]
            sql=sql+order_str
        if(limit):
            if(limit==1):
                sql=sql+" LIMIT 1"
                return self.get_dimensions_one_row(sql)
            else:
                sql=sql+" LIMIT "+limit+", "+skip
                return self.get_dimensions_rows(sql)
        else:
            return self.get_dimensions_rows(sql)

    def __change_filter(self,input):
        if(input==0):
            return "="
        if(input==1):
            return ">"
        if(input==-1):
            return "<"

    def __dispose_except(self,sql):
            info = sys.exc_info()
            err_logger = LogRec.get_logger(Config.ERRLOGGER)
            for file, lineno, function, text in traceback.extract_tb(info[2]):
                err_str = file, "line:", lineno, "in", function
                err_logger.error(err_str)
            err_str = "** %s: %s" % info[:2]
            err_logger.error(err_str)

    def __del__(self):
        if self.__con:
            self.__con.close()

    def destory(self):
        if self.__con:
            self.__con.close()
            self.__con = None

