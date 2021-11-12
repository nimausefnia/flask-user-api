from flask import Flask,request,jsonify
from flask_jwt_extended.utils import create_refresh_token
from flask_restful import Api,Resource
import pymssql
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app=Flask(__name__)
api=Api(app)
app.config["JWT_SECRET_KEY"] = "fdsjhkfdsisdfiosfd12"  
jwt=JWTManager(app)

conn= pymssql.connect(server='localhost',user='SA',password='75369512Th',database='diver')
cursor = conn.cursor(as_dict=True)



class UserLogin(Resource):
    
    def post(self):
        json_data = request.get_json(force=True)
        phone = json_data["phone"]
        password = json_data["password"]
        x = cursor.execute('SELECT * FROM diver.dbo.Profile WHERE phone=%s', (phone))
        y = cursor.execute('SELECT * FROM diver.dbo.Profile WHERE password=%s', (password))
        if not phone == x and password == y:
            return jsonify({"msg": "wrong phone or password number"}), 401
          
        access_token = create_access_token(identity=phone)
        refresh_token=create_refresh_token(identity=phone)
        return jsonify(access_token=access_token,refresh_token=refresh_token)
   

class Profile(Resource):
    
    def get(self):
        cursor.execute("""
            SELECT id, name, lastname
            FROM diver.dbo.Profile;

        """)
        a=cursor.fetchall()
        return a

    @jwt_required()
    def post(self):
        json_data =request.get_json(force=True)
        id = json_data['id']
        name = json_data['name']
        lastname= json_data['lastname']
        phone = json_data['phone']
        password= json_data['password']
        cursor.executemany(
            "INSERT INTO diver.dbo.Profile VALUES (%d,%s,%s,%d,%d)",
            [(id,name,lastname,phone,password)]

        )
        conn.commit()
        return {name:'your profile submited'}
        


          
        
                            



class GetOnePerson(Resource):
    def get(self,name):
                
        with pymssql.connect(server='localhost',user='SA',password='75369512Th',database='diver'):
            with conn.cursor(as_dict=True) as cursor:
                cursor.execute("""
                CREATE PROCEDURE FindProfile
                    @name VARCHAR(100)
                    
                AS BEGIN
                    SELECT * FROM Profile WHERE name = @name
                END
                """)
                a=cursor.callproc('FindProfile', (name,))
                return a

                

            

        
        


api.add_resource(Profile,'/')    
api.add_resource(GetOnePerson,'/<string:name>')
api.add_resource(UserLogin,'/auth')






if __name__=='__main__':
    app.run(debug=True)
