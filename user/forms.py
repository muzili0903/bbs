# -*- coding:utf-8 -*-
'''
@project : bbs
@Time    : 19-1-24 下午7:55
@Author  : muzili
@File    : forms
'''
from django import forms

from user.models import User


# class RegisterFrom(forms.Form):
#     SEX = (
#         ('M', '男性'),
#         ('F', '女性'),
#         ('S', '保密'),
#     )
#     nickname = forms.CharField(max_length=16)
#     password = forms.CharField(max_length=128)
#     icon = forms.ImageField()
#     age = forms.IntegerField(default=18)
#     grade = forms.CharField(max_length=8, choices=SEX)


class RegisterFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'password', 'icon', 'age', 'grade']

    password2 = forms.CharField(max_length=128)

    # 使用clean_来验证字段
    def clean_password2(self):
        '''验证两次输入的密码'''
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            # 抛出错误，可以传一个字符串
            raise forms.ValidationError('两次密码不一致')
