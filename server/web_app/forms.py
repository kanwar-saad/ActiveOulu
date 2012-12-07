# -*- coding: utf-8 -*-

from django import forms
from datetime import datetime


#import datetime
class FeedbackForm(forms.Form):
    # Q1
    q1 = forms.ChoiceField(required=True, choices=[("male", "Male"),("female", "Female")], widget=forms.RadioSelect)
    # Q2
    q2 = forms.ChoiceField(required=True, choices=[("a", "12 years old or younger"),
                                                            ("b", "13-19 years"),
                                                            ("c", "20-29 years"),
                                                            ("d", "30-39 years"),
                                                            ("e", "40-49 years"),
                                                            ("f", "50-59 years"),
                                                            ("g", "60-69 years"),
                                                            ("h", "70 years or older")], 
                                                        widget=forms.RadioSelect)
    # Q3
    #test_field = forms.CharField(max_length=100, required=True)
    q3_city = forms.CharField(max_length=64, required=True)
    q3_country = forms.CharField(max_length=64, required=True)
    # Q4
    q4 = forms.ChoiceField(required=False, choices=[("a", "No"),("b", "0-2 Years"),("c", "3-5 Years"),("d", "Over 5 Years")], widget=forms.RadioSelect)
    # Q5
    q5 = forms.ChoiceField(required=True, choices=[("a", "Elementary or Middle School"),
                                                    ("b", "Upper Secondary School / Vocational School"),
                                                    ("c", "c.    Bachelor\'s Degree / Higher Vocational Degree"),
                                                    ("d", "d.   Master\'s Degree or a Doctorate"),
                                                    ("e", "Other, please specify : ")], 
                                                widget=forms.RadioSelect) 
    q5_other = forms.CharField(max_length=64, required=False)
    # Q6
    
    q6 = forms.ChoiceField(required=True, choices=[("a", "Health care and social work"),
                                                            ("b", "Industry"),
                                                            ("c", "Education & Research"),
                                                            ("d", "Business"), 
                                                            ("e", "Creative Professions"), 
                                                            ("f", "Logistics"), 
                                                            ("g", "Government"), 
                                                            ("h", "Military and Security"), 
                                                            ("i", "Communication"), 
                                                            ("j", "Technology"), 
                                                            ("k", "Other")], 
                                                        widget=forms.RadioSelect)
    q6_title = forms.CharField(max_length=64, required=True)
    # Q7
    q7 = forms.DateTimeField(required=True, initial=datetime.now, widget=forms.DateTimeInput) 
    #q7 = forms.DateField(required=True, initial=datetime.date.today, widget=forms.DateInput) 
    # Q8

    q8 = forms.CharField(max_length=200, required=True)
    # Q9

    q9 = forms.CharField(max_length=200, required=True)
    # Q10

    q10 = forms.CharField(max_length=200, required=True)
    # Q11
    q11 = forms.ChoiceField(required=True, choices=[("a", "0"),
                                                            ("b", "1"),
                                                            ("c", "2"),
                                                            ("d", "3"),     
                                                            ("e", "4"),
                                                            ("k", "5")],
                                                        widget=forms.RadioSelect) 
    q11_why = forms.CharField(max_length=200, required=True)
    # Q12
    q12 = forms.ChoiceField(required=True, choices=[("a", "Yes"),
                                                    ("b", "No")],
                                                        widget=forms.RadioSelect) 
    q12_how = forms.CharField(max_length=200, required=False)

    # Q13

    q13 = forms.ChoiceField(required=True, choices=[("a", "0"),
                                                    ("b", "1"),
                                                    ("b", "2"),
                                                    ("b", "3"),
                                                    ("b", "4"),
                                                    ("b", "5")],
                                                        widget=forms.RadioSelect) 
    q13_why = forms.CharField(max_length=200, required=True)
    # Q14
    
    q14 = forms.ChoiceField(required=True, choices=[("a", "Through Urban Echoes mobile service"),
                                                    ("b", "Through other route, which? ")],
                                                        widget=forms.RadioSelect) 
    q14_which = forms.CharField(max_length=200, required=False)
    q14_how = forms.CharField(max_length=200, required=False)
    # Q15
    q15 = forms.CharField(max_length=200, required=False)

    # contact
    
    name = forms.CharField(max_length=64, required=False)
    email = forms.EmailField(required=False)
    """
    """
    def clean_q5_other(self):
        if (self.cleaned_data.get('q5') == 'e'):
            if not self.cleaned_data.get('q5_other'):
                raise forms.ValidationError(u'Please Specify Q5 Other')
        if (self.cleaned_data.get('q5_other') and (self.cleaned_data.get('q5') != 'e')):
            return ""

        return self.cleaned_data.get('q5_other')            


    def clean_q12_how(self):
        if (self.cleaned_data.get('q12') == 'a'):
            if not self.cleaned_data.get('q12_how'):
                raise forms.ValidationError(u'Please Specify Q12 How')
        if (self.cleaned_data.get('q12_how') and (self.cleaned_data.get('q12') != 'a')):
            return ""

        return self.cleaned_data.get('q12_how')            


    def clean_q14_which(self):
        if (self.cleaned_data.get('q14') == 'b'):
            if not self.cleaned_data.get('q14_which'):
                raise forms.ValidationError(u'Please Specify Q14 Which')
        if (self.cleaned_data.get('q14_which') and (self.cleaned_data.get('q14') != 'b')):
            return ""

        return self.cleaned_data.get('q14_which')

    def clean_q14_how(self):
        if (self.cleaned_data.get('q14') == 'a'):
            if not self.cleaned_data.get('q14_how'):
                raise forms.ValidationError(u'Please Specify Q14 How')
        if (self.cleaned_data.get('q14_how') and (self.cleaned_data.get('q14') != 'a')):
            return ""

        return self.cleaned_data.get('q14_how')









class FeedbackForm_fi(forms.Form):
    # Q1
    q1 = forms.ChoiceField(required=True, choices=[("male", "mies"),("female", "nainen")], widget=forms.RadioSelect)
    # Q2
    q2 = forms.ChoiceField(required=True, choices=[("a", "12 vuotta tai alle"),
                                                            ("b", "13-19"),
                                                            ("c", "20-29"),
                                                            ("d", "30-39"),
                                                            ("e", "40-49"),
                                                            ("f", "50-59"),
                                                            ("g", "60-69"),
                                                            ("h", "70 vuotta tai yli")], 
                                                        widget=forms.RadioSelect)
    # Q3
    #test_field = forms.CharField(max_length=100, required=True)
    q3_city = forms.CharField(max_length=64, required=True)
    q3_country = forms.CharField(max_length=64, required=True)
    # Q4
    q4 = forms.ChoiceField(required=False, choices=[("a", "En"),("b", "0-2 vuotta"),("c", "3-5 vuotta"),("d", "yli 5 vuotta")], widget=forms.RadioSelect)
    # Q5
    q5 = forms.ChoiceField(required=True, choices=[("a", "Peruskoulun pätöistus"),
                                                    ("b", "Ylioppilas tai ammattitutkinto"),
                                                    ("c", "Alempi korkeakoulututkinto"),
                                                    ("d", "Ylempi korkeakoulututkinto"),
                                                    ("e", "Muu, mikäOD")], 
                                                widget=forms.RadioSelect) 
    q5_other = forms.CharField(max_length=64, required=False)
    # Q6
    
    q6 = forms.ChoiceField(required=True, choices=[("a", "Sosiaali- ja terveysala"),
                                                            ("b", "Teollisuuden ala"),
                                                            ("c", "Opetus ja tutkimus"),
                                                            ("d", "Kaupallinen ala"), 
                                                            ("e", "Luovat alat"), 
                                                            ("f", "Liikenne ja logistiikka"), 
                                                            ("g", "Hallinto"), 
                                                            ("h", "Turvallisuus ja maanpuolustus"), 
                                                            ("i", "ViestintäD"), 
                                                            ("j", "Tekniikan ala"), 
                                                            ("k", "Muu")], 
                                                        widget=forms.RadioSelect)
    q6_title = forms.CharField(max_length=64, required=True)
    # Q7
    q7 = forms.DateTimeField(required=True, initial=datetime.now, widget=forms.DateTimeInput) 
    #q7 = forms.DateField(required=True, initial=datetime.date.today, widget=forms.DateInput) 
    # Q8

    q8 = forms.CharField(max_length=200, required=True)
    # Q9

    q9 = forms.CharField(max_length=200, required=True)
    # Q10

    q10 = forms.CharField(max_length=200, required=True)
    # Q11
    q11 = forms.ChoiceField(required=True, choices=[("a", "0"),
                                                            ("b", "1"),
                                                            ("c", "2"),
                                                            ("d", "3"),     
                                                            ("e", "4"),
                                                            ("k", "5")],
                                                        widget=forms.RadioSelect) 
    q11_why = forms.CharField(max_length=200, required=True)
    # Q12
    q12 = forms.ChoiceField(required=True, choices=[("a", "Kyllä"),
                                                    ("b", "Ei")],
                                                        widget=forms.RadioSelect) 
    q12_how = forms.CharField(max_length=200, required=False)

    # Q13

    q13 = forms.ChoiceField(required=True, choices=[("a", "0"),
                                                    ("b", "1"),
                                                    ("b", "2"),
                                                    ("b", "3"),
                                                    ("b", "4"),
                                                    ("b", "5")],
                                                        widget=forms.RadioSelect) 
    q13_why = forms.CharField(max_length=200, required=True)
    # Q14
    
    q14 = forms.ChoiceField(required=True, choices=[("a", "Kaupunkikaikuja-mobiilipalvelun kautta"),
                                                    ("b", "Muuta reittiämitäOB ")],
                                                        widget=forms.RadioSelect) 
    q14_which = forms.CharField(max_length=200, required=False)
    q14_how = forms.CharField(max_length=200, required=False)
    # Q15
    q15 = forms.CharField(max_length=200, required=False)

    # contact
    
    name = forms.CharField(max_length=64, required=False)
    email = forms.EmailField(required=False)
    """
    """
    def clean_q5_other(self):
        if (self.cleaned_data.get('q5') == 'e'):
            if not self.cleaned_data.get('q5_other'):
                raise forms.ValidationError(u'Please Specify Q5 Other')
        if (self.cleaned_data.get('q5_other') and (self.cleaned_data.get('q5') != 'e')):
            return ""

        return self.cleaned_data.get('q5_other')            


    def clean_q12_how(self):
        if (self.cleaned_data.get('q12') == 'a'):
            if not self.cleaned_data.get('q12_how'):
                raise forms.ValidationError(u'Please Specify Q12 How')
        if (self.cleaned_data.get('q12_how') and (self.cleaned_data.get('q12') != 'a')):
            return ""

        return self.cleaned_data.get('q12_how')            


    def clean_q14_which(self):
        if (self.cleaned_data.get('q14') == 'b'):
            if not self.cleaned_data.get('q14_which'):
                raise forms.ValidationError(u'Please Specify Q14 Which')
        if (self.cleaned_data.get('q14_which') and (self.cleaned_data.get('q14') != 'b')):
            return ""

        return self.cleaned_data.get('q14_which')

    def clean_q14_how(self):
        if (self.cleaned_data.get('q14') == 'a'):
            if not self.cleaned_data.get('q14_how'):
                raise forms.ValidationError(u'Please Specify Q14 How')
        if (self.cleaned_data.get('q14_how') and (self.cleaned_data.get('q14') != 'a')):
            return ""

        return self.cleaned_data.get('q14_how')














