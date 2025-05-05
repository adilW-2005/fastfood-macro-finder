# from config import db
# from models import User, nutrition_info

# new_user = User(username="testuser", password="hashedpassword")
# db.session.add(new_user)
# db.session.commit()

# log = nutrition_info(user_id=new_user.id, food_id="12345", calories=200, protein=10, fat=5, carbs=30)
# db.session.add(log)
# db.session.commit()

# # ✅ Check logs
# print(new_user.nutrition_logs)  # Should return a list of logs
