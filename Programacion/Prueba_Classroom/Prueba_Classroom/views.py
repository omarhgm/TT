import pickle
import os.path
import json
from django.http import HttpResponse
from django.template import Template, Context
# from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Course(object):
    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id


def grupos(request):
    SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
              'https://www.googleapis.com/auth/classroom.rosters',
              'https://www.googleapis.com/auth/classroom.rosters.readonly',
              'https://www.googleapis.com/auth/classroom.profile.emails',
              'https://www.googleapis.com/auth/classroom.profile.photos']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:/Users/OmarGM/Documents/TT/Programacion/Prueba_Classroom/Prueba_Classroom/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])
    Cursos = []

    if not courses:
        print('No courses found.')
    else:
        print('Courses:')
        for course in courses:
            Cursos.append(Course(course['name'], course['id']))
            print(course['name'])
            resultA = service.courses().students().list(
                courseId=course['id']).execute()
            alumnos = resultA['students']
            resultP = service.courses().teachers().list(
                courseId=course['id']).execute()
            profesores = resultP['teachers']
            for alumno in alumnos:
                print(alumno['profile']['name'])
            for profesor in profesores:
                print(profesor['profile']['name'])

    nombreA = alumnos[0]['profile']['name']['givenName']

    doc_externo = open(
        "C:/Users/OmarGM/Documents/TT/Programacion/Prueba_Classroom/Prueba_Classroom/plantillas/tabla.html")
    plt = Template(doc_externo.read())
    doc_externo.close()

    ctx = Context({"cursos": courses, "alumnos": alumnos,
                   "profesores": profesores})

    documento = plt.render(ctx)

    return HttpResponse(documento)
