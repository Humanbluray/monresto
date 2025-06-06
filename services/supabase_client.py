import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase_client = create_client(url, key)


# res = supabase_client.auth.sign_in_with_password(
#     {'email': 'janedoe@mail.com', "password": '123456'}
# )
#
# user_id = res.user.id
# print(user_id)
#
# resp = supabase_client.table('users').select('restaurant_id').eq('uid', user_id).single().execute()
# id_resto = resp.data['restaurant_id']
# print(id_resto)
#
# resp = supabase_client.table('abonnements').select('date_debut', 'date_fin', 'actif').single().execute()
# print(resp.data)
