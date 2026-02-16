from backend.database import initialize_database
from backend.user_service import seed_default_users
from backend.pod_service import seed_default_pods

if __name__ == "__main__":   # INITIALLY RUN TO INITIALIZE DATABASE AND CREATE SOME USERS AND PODS
    initialize_database()
    seed_default_users()
    seed_default_pods()
    print("Database initialized with users and pods.")
