# -*- coding: utf-8 -*-

from django.db import models
import datetime, sys
from djangotoolbox.fields import *

# Create your models here.

class BTActivity(models.Model):
    devID = models.IntegerField(blank=False)
    activityTime = models.DateTimeField(blank=False)
    activity = models.IntegerField(blank=False)


class BTDevice(models.Model):
    devID = models.IntegerField(blank=False)
    devName = models.CharField(max_length=64, blank=True)
    devLocLat = models.CharField(blank=False, max_length=20)
    devLocLong = models.CharField(blank=False, max_length=20)
    scanTime = models.DateTimeField(blank=False)

class Feedback(models.Model):
    # Q1
    q1 = models.CharField(max_length=1, blank=False, choices=[("male", "Male"),("female", "Female")])
    # Q2
    q2 = models.CharField(max_length=1,blank=False, choices=[("a", "12 years old or younger"),
                                                            ("b", "13-19 years"),
                                                            ("c", "20-29 years"),
                                                            ("d", "30-39 years"),
                                                            ("e", "40-49 years"),
                                                            ("f", "50-59 years"),
                                                            ("g", "60-69 years"),
                                                            ("h", "70 years or older")])
    # Q3
    #test_field = models.CharField(max_length=100, blank=False)
    q3_city = models.CharField(max_length=64, blank=False)
    q3_country = models.CharField(max_length=64, blank=False)
    # Q4
    q4 = models.CharField(max_length=1,blank=True, choices=[("a", "No"),("b", "0-2 Years"),("c", "3-5 Years"),("d", "Over 5 Years")])
    # Q5
    q5 = models.CharField(max_length=1,blank=False, choices=[("a", "Elementary or Middle School"),
                                                    ("b", "Upper Secondary School / Vocational School"),
                                                    ("c", "c.    Bachelor\'s Degree / Higher Vocational Degree"),
                                                    ("d", "d.   Master\'s Degree or a Doctorate"),
                                                    ("e", "Other, please specify : ")])
    q5_other = models.CharField(max_length=64, blank=True)
    # Q6

    q6 = models.CharField(max_length=1,blank=False, choices=[("a", "Health care and social work"),
                                                            ("b", "Industry"),
                                                            ("c", "Education & Research"),
                                                            ("d", "Business"),
                                                            ("e", "Creative Professions"),
                                                            ("f", "Logistics"),
                                                            ("g", "Government"),
                                                            ("h", "Military and Security"),
                                                            ("i", "Communication"),
                                                            ("j", "Technology"),
                                                            ("k", "Other")])
    q6_title = models.CharField(max_length=64, blank=False)
    # Q7
    q7 = models.DateTimeField(blank=False)
    # Q8

    q8 = models.CharField(max_length=200, blank=False)
    # Q9

    q9 = models.CharField(max_length=200, blank=False)
    # Q10

    q10 = models.CharField(max_length=200, blank=False)
    # Q11
    q11 = models.CharField(max_length=1,blank=False, choices=[("a", "0"),
                                                            ("b", "1"),
                                                            ("c", "2"),
                                                            ("d", "3"),
                                                            ("e", "4"),
                                                            ("k", "5")])
                                                        
    q11_why = models.CharField(max_length=200, blank=False)
    # Q12
    q12 = models.CharField(max_length=1,blank=False, choices=[("a", "Yes"),
                                                    ("b", "No")])
    q12_how = models.CharField(max_length=200, blank=True)

    # Q13

    q13 = models.CharField(max_length=1,blank=False, choices=[("a", "0"),
                                                    ("b", "1"),
                                                    ("b", "2"),
                                                    ("b", "3"),
                                                    ("b", "4"),
                                                    ("b", "5")])
    q13_why = models.CharField(max_length=200, blank=False)
    # Q14

    q14 = models.CharField(max_length=1,blank=False, choices=[("a", "Through Urban Echoes mobile service"),
                                                    ("b", "Through other route, which? ")])
    q14_which = models.CharField(max_length=200, blank=True)
    q14_how = models.CharField(max_length=200, blank=True)
    # Q15
    q15 = models.CharField(max_length=200, blank=True)

    # contact

    name = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True)
    datetime = models.DateTimeField(blank=False)


class Feedback_fi(models.Model):
    # Q1
    q1 = models.CharField(max_length=1, blank=False, choices=[("male", "mies"),("female", "nainen")])
    # Q2
    q2 = models.CharField(max_length=1,blank=False, choices=[("a", "12 vuotta tai alle"),
                                                            ("b", "13-19"),
                                                            ("c", "20-29"),
                                                            ("d", "30-39"),
                                                            ("e", "40-49"),
                                                            ("f", "50-59"),
                                                            ("g", "60-69"),
                                                            ("h", "70 vuotta tai yli")])
    # Q3
    #test_field = models.CharField(max_length=100, blank=False)
    q3_city = models.CharField(max_length=64, blank=False)
    q3_country = models.CharField(max_length=64, blank=False)
    # Q4
    q4 = models.CharField(max_length=1,blank=True, choices=[("a", "En"),("b", "0-2 vuotta"),("c", "3-5 vuotta"),("d", "yli 5 vuotta")])
    # Q5
    q5 = models.CharField(max_length=1,blank=False, choices=[("a", "Peruskoulun pätöistus"),
                                                    ("b", "Ylioppilas tai ammattitutkinto"),
                                                    ("c", "Alempi korkeakoulututkinto"),
                                                    ("d", "Ylempi korkeakoulututkinto"),
                                                    ("e", "Muu, mikäOD")])
    q5_other = models.CharField(max_length=64, blank=True)
    # Q6

    q6 = models.CharField(max_length=1,blank=False, choices=[("a", "Sosiaali- ja terveysala"),
                                                            ("b", "Teollisuuden ala"),
                                                            ("c", "Opetus ja tutkimus"),
                                                            ("d", "Kaupallinen ala"),
                                                            ("e", "Luovat alat"),
                                                            ("f", "Liikenne ja logistiikka"),
                                                            ("g", "Hallinto"),
                                                            ("h", "Turvallisuus ja maanpuolustus"),
                                                            ("i", "ViestintäD"),
                                                            ("j", "Tekniikan ala"),
                                                            ("k", "Muu")])
    q6_title = models.CharField(max_length=64, blank=False)
    # Q7
    q7 = models.DateTimeField(blank=False)
    # Q8

    q8 = models.CharField(max_length=200, blank=False)
    # Q9

    q9 = models.CharField(max_length=200, blank=False)
    # Q10

    q10 = models.CharField(max_length=200, blank=False)
    # Q11
    q11 = models.CharField(max_length=1,blank=False, choices=[("a", "0"),
                                                            ("b", "1"),
                                                            ("c", "2"),
                                                            ("d", "3"),
                                                            ("e", "4"),
                                                            ("k", "5")])
                                                        
    q11_why = models.CharField(max_length=200, blank=False)
    # Q12
    q12 = models.CharField(max_length=1,blank=False, choices=[("a", "KylläB"),
                                                    ("b", "Ei")])
    q12_how = models.CharField(max_length=200, blank=True)

    # Q13

    q13 = models.CharField(max_length=1,blank=False, choices=[("a", "0"),
                                                    ("b", "1"),
                                                    ("b", "2"),
                                                    ("b", "3"),
                                                    ("b", "4"),
                                                    ("b", "5")])
    q13_why = models.CharField(max_length=200, blank=False)
    # Q14

    q14 = models.CharField(max_length=1,blank=False, choices=[("a", "Kaupunkikaikuja-mobiilipalvelun kautta"),
                                                    ("b", "Muuta reittiämitäOB ")])
    q14_which = models.CharField(max_length=200, blank=True)
    q14_how = models.CharField(max_length=200, blank=True)
    # Q15
    q15 = models.CharField(max_length=200, blank=True)

    # contact

    name = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True)
    datetime = models.DateTimeField(blank=False)
