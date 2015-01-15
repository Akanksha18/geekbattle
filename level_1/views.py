import json
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Question
from .models import Answer
from django.http import HttpResponse,HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse


@login_required(login_url=reverse('user:login'))
def home(request):
	 return render(request,'level_1/home.html')	


@login_required(login_url=reverse('user:login'))
def start(request):
	if request.method == "GET":
		return render(request,'level_1/home.html')
	elif request.method == "POST":
		obj = Answer.objects.get(user=request.user)
		if obj.s1 >= 0:
		 return render(request,'level_1/home.html')		
		choice = request.POST.get('re')
		qid = request.POST.get('qid1')
		if qid is None:
			return render(request,'level_1/display.html',{'qid' : 1})
		answer_list = json.loads(obj.answer_list)
		if str(choice) == str(answer_list[int(qid)-1]):
			choice = "0"
		answer_list[int(qid)-1]=int(choice)
		obj.answer_list=answer_list
		obj.save()
		return render(request,'level_1/display.html',{'qid' : qid})

@login_required(login_url=reverse('user:login'))
def question(request,qid):
	return render(request,'level_1/question.html',{'qid' : qid})

@login_required(login_url=reverse('user:login'))
def submit(request):
	obj = Answer.objects.get(user=request.user)	
	answer_list = json.loads(obj.answer_list)
	obj.s1=0
	temp=1
	question_list = Question.objects.all()
	for i in question_list:
		question_obj = Question.objects.get(id=str(temp))
		if answer_list[temp] == question_obj.answer:
			obj.s1 = int(obj.s1) +1
		temp += 1
	obj.s1 = (float(obj.s1)/(temp-1))*100
	obj.save()
	return HttpResponseRedirect(reverse('level_1:home'))

@login_required(login_url=reverse('user:login'))
def mark(request):
	qid = request.POST.get('qid2')
	obj=Question.objects.get(id=str(qid))
	answer_obj = Answer.objects.get(user=request.user)	
	data = json.loads(answer_obj.active_status_list)
	data[int(qid)-1]=int(request.POST.get('name'))
	answer_obj.active_status_list=data
	answer_obj.save()
	obj.save()
	return render(request,'level_1/display.html',{'qid' : qid})

@login_required(login_url=reverse('user:login'))
def question_list(request):
	question_list = Question.objects.all()
	question_list_array = []
  	for i in question_list:
  		question_list_dic = question_list_dictionary(request,i)
   		question_list_array.append(question_list_dic)
  	return HttpResponse(json.dumps(question_list_array,cls=DjangoJSONEncoder), content_type="application/json")


def question_list_dictionary(request,question):
	temp = {}
	obj = Answer.objects.get(user=request.user)	
	data = json.loads(obj.answer_list)
	temp["id"] = question.id
	temp["answer"] = data[question.id-1]
	data = json.loads(obj.active_status_list)
   	temp["active_status"] = data[question.id-1]
   	temp["choice_1"] = question.choice_1
	temp["choice_2"] = question.choice_2
	temp["choice_3"] = question.choice_3
	temp["choice_4"] = question.choice_4
   	temp["description"] = question.description
	temp["count"]=0	
	data = json.loads(obj.answer_list)
	index=0
	for i in data:
		if data[index] != 0:
			temp["count"] += 1
		index += 1
	return temp

@login_required(login_url=reverse('user:login'))
def question_json(request,qid):
	question_array = []
	question_obj = Question.objects.get(id=qid)
	data=question_list_dictionary(request,question_obj)
	question_array.append(data)
	return HttpResponse(json.dumps(question_array,cls=DjangoJSONEncoder), content_type="application/json")

def answer_json(request):
	answer_array = []	
	answer_obj = Answer.objects.get(user=request.user)
	data=answer_dictionary(request,answer_obj)
	answer_array.append(data)
	return HttpResponse(json.dumps(answer_array,cls=DjangoJSONEncoder), content_type="application/json")

def answer_dictionary(request,answer1):
	temp = {}
	temp["user"] = answer1.user.username
	temp["answer_list"] = json.loads(answer1.answer_list)
	temp["active_status_list"] = json.loads(answer1.active_status_list)
	temp["s1"] = answer1.s1
	temp["s2"] = answer1.s2
	temp["s3"] = answer1.s3
	return temp        
