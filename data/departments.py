"""
BCC Departments and Majors data
Source: https://www.bcc.cuny.edu/academics/academic-programs/
Used to power the Department -> Major dropdown filters in the job search app.
"""

DEPARTMENTS = {
    "All Departments": ["All Majors"],
    "Art and Music": ["All Majors", "Digital Design", "Studio Art"],
    "Biological Sciences": ["All Majors", "Biotechnology", "Horticulture", "Animal Care Management", "Biology"],
    "Business and Information Systems": ["All Majors", "Accounting", "Computer Information Systems", "Marketing",
        "Medical Office Assistant", "Office Administration and Technology", "Paralegal and Legal Studies",
        "Business Administration: Accounting", "Business Administration: Computer Programming",
        "Business Administration: Management", "Business Administration: Marketing"],
    "Chemistry and Chemical Technology": ["All Majors", "Earth Systems & Environmental Science", "Chemistry", "Forensics"],
    "Communication Arts and Sciences": ["All Majors", "Media Studies", "Performing Arts", "Speech Pathology", "Media and Digital Film Production"],
    "Education and Academic Literacy": ["All Majors", "Early Childhood and Childhood Education", "Secondary Education",
        "Education", "Exercise Science and Kinesiology", "Therapeutic Recreation",
        "Assistant of Children with Special Needs", "Bilingual Early Childhood Assistant", "Early Childhood Assistant"],
    "Engineering, Physics and Technology": ["All Majors", "Automotive Technology", "Cybersecurity and Networking",
        "Electronic Engineering Technology", "Engineering Science", "Physics", "Automotive Technician"],
    "Mathematics and Computer Science": ["All Majors", "Computer Science", "Mathematics"],
    "Modern Languages": ["All Majors", "Spanish"],
    "Nursing and Allied Health Sciences": ["All Majors", "Medical Laboratory Technician", "Nuclear Medicine Technology",
        "Nursing", "Radiologic Technology", "Dietetics and Nutrition Science", "Health Sciences", "Public Health"],
    "Social Sciences": ["All Majors", "Criminal Justice", "Black and Latinx Studies", "Human Services",
        "Political Science", "Psychology", "Sociology"],
    "English": ["All Majors", "English"],
    "History": ["All Majors", "History"],
    "General / Liberal Arts": ["All Majors", "Liberal Arts and Sciences"],
}

ALL_DEPARTMENTS_LABEL = "All Departments"
ALL_MAJORS_LABEL = "All Majors"
