from backend.database import get_connection



# FUNCTION FOR CREATING PODS - WILL ALSO BE USED FOR ADDING USERS VIA CONTROLLER UI

def create_pod(name: str, track_id: str, status: str = "running"):
    """
    Inserts a new pod into database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pods (name, track_id, status)
        VALUES (?, ?, ?)
    """, (name, track_id, status))

    conn.commit()
    conn.close()



# GET ALL PODS

def get_all_pods():
    """
    Returns list of all pods.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pods")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# GET POD BY NAME

def get_pod_by_name(name: str):
    """
    Returns single pod by name.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM pods WHERE name = ?",
        (name,)
    )

    pod = cursor.fetchone()
    conn.close()

    if pod:
        return dict(pod)

    return None


# UPDATE POD STATUS

def update_pod_status(pod_id: int, new_status: str):
    """
    Updates pod operational status.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pods
        SET status = ?
        WHERE id = ?
    """, (new_status, pod_id))

    conn.commit()
    conn.close()


# ADD FEW DEFAULT PODS INITIALLY - REST CAN BE ADDED LATER VIA CONTROLLER UI WHEN DEVELOPPED 

def seed_default_pods():
    """
    Inserts default pods if table empty.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as count FROM pods")
    count = cursor.fetchone()["count"]
    conn.close()

    if count == 0:
        create_pod("Pod-A", "Track-1", "running")
        create_pod("Pod-B", "Track-1", "running")
        create_pod("Pod-C", "Track-2", "maintenance")

