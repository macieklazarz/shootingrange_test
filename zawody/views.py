from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.shortcuts import reverse, render
from .forms import ZawodyModelForm, SedziaModelForm, ZawodyGrupaModelForm, ZawodyDynamicModelForm, SedziaDynamicModelForm, SedziaModelFormNew, SedziaDynamicModelFormNew, ZawodnicyDruzynyModelForm, DruzynaModelForm
from .models import Sedzia, SedziaDynamic, Zawody, Turniej, ZawodyGrupa, ZawodyDynamic, Druzyna, ZawodnicyDruzyny
# from wyniki.views import sedziowie_lista
from django.shortcuts import redirect
# from account.views import sedziowie_lista
from mainapp.views import nazwa_turnieju
from account.models import Account

# Create your views here.


class StronaStartowaListView(ListView):
	template_name = "zawody/turniej_list.html"

	def get_queryset(self):
		return Turniej.objects.filter(turniej_archiwalny=False)

class TurniejArchiwalnyListView(ListView):
	template_name = "zawody/turniej_archive_list.html"

	def get_queryset(self):
		return Turniej.objects.filter(turniej_archiwalny=True)


class ZawodyListView(LoginRequiredMixin, ListView):
	login_url = '/start/'
	template_name = "zawody/zawody_lista.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_queryset(self, **kwargs):
		return Zawody.objects.filter(turniej=self.kwargs['pk'])

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(ZawodyListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')

class ZawodyDynamicListView(LoginRequiredMixin, ListView):
	login_url = '/start/'
	template_name = "zawody/zawody_dynamic_lista.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_queryset(self, **kwargs):
		return ZawodyDynamic.objects.filter(turniej=self.kwargs['pk'])

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(ZawodyDynamicListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')


class ZawodyCreateView(LoginRequiredMixin, CreateView):
	login_url = 'start'
	template_name = "zawody/zawody_create.html"
	form_class = ZawodyModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_success_url(self):
		return reverse("zawody_lista", kwargs={'pk':self.kwargs['pk']})
		return super(ZawodyCreateView, self).form_valid(form)
	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(ZawodyCreateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect("not_authorized")

class ZawodyDynamicCreateView(LoginRequiredMixin, CreateView):
	login_url = 'start'
	template_name = "zawody/zawody_create.html"
	form_class = ZawodyDynamicModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_success_url(self):
		return reverse("zawody_dynamic_lista", kwargs={'pk':self.kwargs['pk']})
		return super(ZawodyDynamicCreateView, self).form_valid(form)
	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(ZawodyDynamicCreateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect("not_authorized")


class ZawodyEditView(LoginRequiredMixin,UpdateView):
	login_url = 'start'
	template_name = "zawody/zawody_edit.html"
	form_class = ZawodyModelForm
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		return context

	def get_queryset(self):
		return Zawody.objects.all()

	def get_success_url(self):
		return reverse("zawody_lista", kwargs={'pk':self.kwargs['pk_turniej']})
		return super(TurniejEditView, self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(ZawodyEditView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')

class ZawodyDynamicEditView(LoginRequiredMixin,UpdateView):
	login_url = 'start'
	template_name = "zawody/zawody_edit.html"
	form_class = ZawodyDynamicModelForm
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		return context

	def get_queryset(self):
		return ZawodyDynamic.objects.all()

	def get_success_url(self):
		return reverse("zawody_dynamic_lista", kwargs={'pk':self.kwargs['pk_turniej']})
		return super(TurniejEditView, self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(ZawodyDynamicEditView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')



class ZawodyDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "zawody/zawody_delete.html"
	context_object_name = 'zawody'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		return context

	def get_queryset(self):
		return Zawody.objects.all()

	def get_success_url(self):
		return reverse("zawody_lista", kwargs={'pk': self.kwargs['pk_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(ZawodyDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')

class ZawodyDynamicDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "zawody/zawody_delete.html"
	context_object_name = 'zawody'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		return context

	def get_queryset(self):
		return ZawodyDynamic.objects.all()

	def get_success_url(self):
		return reverse("zawody_dynamic_lista", kwargs={'pk': self.kwargs['pk_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(ZawodyDynamicDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')


class SedziaCreateView(LoginRequiredMixin, CreateView):
	login_url = 'start'
	template_name = "zawody/sedzia_create.html"
	form_class = SedziaModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_success_url(self):
		return reverse("sedzia_lista", kwargs={'pk': self.kwargs['pk']})
		return super(SedziaCreateView, self).form_valid(form)

	def get_form_kwargs(self):
		kwargs = super(SedziaCreateView, self).get_form_kwargs()
		zawody_pk = self.kwargs['pk']
		kwargs.update({'zawody_pk': zawody_pk})
		return kwargs

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(SedziaCreateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')


@csrf_exempt
@login_required(login_url="")
def sedzia_create(request, pk):
	if request.user.rts:

		context={}
		context['pk'] = pk
		context['nazwa_turnieju'] = nazwa_turnieju(pk)

		
		if request.method == 'POST':
			print('post')

			form = SedziaModelFormNew(request.POST, zawody_pk=pk)
			# print(form)
			print(form.errors)
			# print(form.cleaned_data.get('zawody'))
			if form.is_valid():

				zawody = form.cleaned_data.get('zawody')
				sedzia = form.cleaned_data.get('sedzia')
				print(f'zawody: {zawody}')
				print(f'sedzia: {sedzia}')

				for i in zawody:
					zaw = Zawody.objects.filter(id=i)[0]
					for j in sedzia:
						sedz = Account.objects.filter(id=j)[0]
						if not Sedzia.objects.filter(zawody__id=i, sedzia__id=j):
							Sedzia.objects.create(zawody=zaw , sedzia=sedz)



			form = SedziaModelFormNew(zawody_pk=pk)
		else:
			form = SedziaModelFormNew(zawody_pk=pk)

		context['form'] = form

		return render(request, 'zawody/sedzia_create.html', context)

	else:
		return redirect('not_authorized')


class SedziaDynamicCreateView(LoginRequiredMixin, CreateView):
	login_url = 'start'
	template_name = "zawody/sedzia_create.html"
	form_class = SedziaDynamicModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_success_url(self):
		return reverse("sedzia_dynamic_lista", kwargs={'pk': self.kwargs['pk']})
		return super(SedziaCreateView, self).form_valid(form)

	def get_form_kwargs(self):
		kwargs = super(SedziaDynamicCreateView, self).get_form_kwargs()
		zawody_pk = self.kwargs['pk']
		kwargs.update({'zawody_pk': zawody_pk})
		return kwargs

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(SedziaDynamicCreateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')



@csrf_exempt
@login_required(login_url="/start/")
def sedzia_dynamic_create(request, pk):

	if request.user.rts:
		context={}
		context['pk'] = pk
		context['nazwa_turnieju'] = nazwa_turnieju(pk)

		
		if request.method == 'POST':
			print('post')

			form = SedziaDynamicModelFormNew(request.POST, zawody_pk=pk)
			# print(form)
			print(form.errors)
			# print(form.cleaned_data.get('zawody'))
			if form.is_valid():

				zawody = form.cleaned_data.get('zawody')
				sedzia = form.cleaned_data.get('sedzia')
				print(f'zawody: {zawody}')
				print(f'sedzia: {sedzia}')

				for i in zawody:
					zaw = ZawodyDynamic.objects.filter(id=i)[0]
					for j in sedzia:
						sedz = Account.objects.filter(id=j)[0]
						if not SedziaDynamic.objects.filter(zawody__id=i, sedzia__id=j):
							SedziaDynamic.objects.create(zawody=zaw , sedzia=sedz)



			form = SedziaDynamicModelFormNew(zawody_pk=pk)
		else:
			form = SedziaDynamicModelFormNew(zawody_pk=pk)

		context['form'] = form

		return render(request, 'zawody/sedzia_create.html', context)

	else:
		return redirect('not_authorized')

class SedziaListView(LoginRequiredMixin, ListView):
	login_url = 'start'
	template_name = "zawody/sedzia_lista.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Sedzia.objects.filter(zawody__turniej__id=self.kwargs['pk']).order_by('zawody')

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				print(request.user.id)
				return super(SedziaListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')

class SedziaDynamicListView(LoginRequiredMixin, ListView):
	login_url = 'start'
	template_name = "zawody/sedzia_dynamic_lista.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return SedziaDynamic.objects.filter(zawody__turniej__id=self.kwargs['pk']).order_by('zawody')

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				print(request.user.id)
				return super(SedziaDynamicListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')


class SedziaDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "zawody/sedzia_delete.html"
	context_object_name = 'sedzia'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return Sedzia.objects.all()

	def get_success_url(self):
		return reverse("sedzia_lista", kwargs={'pk': self.kwargs['pk_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(SedziaDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')


class SedziaDynamicDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "zawody/sedzia_delete.html"
	context_object_name = 'sedzia'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		# context['rts_lista'] = rts_lista()
		return context

	def get_queryset(self):
		return SedziaDynamic.objects.all()

	def get_success_url(self):
		return reverse("sedzia_dynamic_lista", kwargs={'pk': self.kwargs['pk_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(SedziaDynamicDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')




class ZawodyGrupaListView(LoginRequiredMixin, ListView):
	login_url = '/start/'
	template_name = "zawody/zawody_grupa_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_queryset(self, **kwargs):
		return ZawodyGrupa.objects.all()

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(ZawodyGrupaListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')

class ZawodyGrupaCreateView(LoginRequiredMixin, CreateView):
	login_url = 'start'
	template_name = "zawody/zawody_grupa_create.html"
	form_class = ZawodyGrupaModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_success_url(self):
		return reverse("zawody_grupa_lista", kwargs={'pk':self.kwargs['pk']})
		return super(ZawodyGrupaCreateView, self).form_valid(form)
	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(ZawodyGrupaCreateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect("not_authorized")


class ZawodyGrupaEditView(LoginRequiredMixin,UpdateView):
	login_url = 'start'
	template_name = "zawody/zawody_grupa_edit.html"
	form_class = ZawodyGrupaModelForm
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		return context

	def get_queryset(self):
		return ZawodyGrupa.objects.all()

	def get_success_url(self):
		return reverse("zawody_grupa_lista", kwargs={'pk':self.kwargs['pk_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(ZawodyGrupaEditView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')

class ZawodyGrupaDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "zawody/zawody_grupa_delete.html"
	context_object_name = 'zawody_grupa'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		return context

	def get_queryset(self):
		return ZawodyGrupa.objects.all()

	def get_success_url(self):
		return reverse("zawody_grupa_lista", kwargs={'pk': self.kwargs['pk_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(ZawodyGrupaDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')




@login_required(login_url="/start/")
def druzyny_management(request, pk):
	context = {}
	context['nazwa_turnieju'] = nazwa_turnieju(pk)
	context['pk'] = pk
	context['admin'] = []
	druzyny_admin = Druzyna.objects.filter(administrator=request.user, turniej=nazwa_turnieju(pk)[0])
	for i in druzyny_admin:
		druzyna_sklad = ZawodnicyDruzyny.objects.filter(druzyna=i)
		slownik_druzyna = {'druzyna':i, 'sklad':druzyna_sklad}
		context['admin'].append(slownik_druzyna)

	context['druzyny_usera'] = ZawodnicyDruzyny.objects.filter(zawodnik=request.user)
	# print(context['admin'])

	# print(f'admin druzyny: {}')
	# print(f'admin druzyny: {ZawodnicyDruzyny.objects.all()}')

	if nazwa_turnieju(pk)[0].turniej_druzynowy:
		return render(request, 'zawody/druzyny.html', context)
	else:
		return redirect('not_authorized')



class ZawodnicyDruzynyCreateView(LoginRequiredMixin, CreateView):
	login_url = 'start'
	template_name = "zawody/zawodnicydruzyny_create.html"
	form_class = ZawodnicyDruzynyModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['druzyna_slug'] = self.kwargs['druzyna_slug']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		context['druzyna'] = Druzyna.objects.get(slug=self.kwargs['druzyna_slug'])
		return context

	def get_success_url(self):
		return reverse("druzyny_management", kwargs={'pk':self.kwargs['pk']})
		return super(ZawodnicyDruzynyCreateView, self).form_valid(form)

	def get_initial(self, *args, **kwargs):
		initial = super(ZawodnicyDruzynyCreateView, self).get_initial()
		initial = initial.copy()
		initial['druzyna'] = Druzyna.objects.get(slug=self.kwargs['druzyna_slug'])
		return initial

	def get_form_kwargs(self):
		kwargs = super(ZawodnicyDruzynyCreateView, self).get_form_kwargs()
		kwargs.update({'druzyna_slug': self.kwargs['druzyna_slug']})
		# kwargs.update({'pk': self.kwargs['pk']})
		return kwargs

	def dispatch(self, request, *args, **kwargs):
		try:
			if nazwa_turnieju(self.kwargs["pk"])[0].turniej_druzynowy and Druzyna.objects.filter(slug=self.kwargs["druzyna_slug"], administrator=self.request.user).count() > 0:
				return super(ZawodnicyDruzynyCreateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect("not_authorized")
			# return super(ZawodnicyDruzynyCreateView, self).dispatch(request, *args, **kwargs)


class DruzynaCreateView(LoginRequiredMixin, CreateView):
	login_url = 'start'
	template_name = "zawody/druzyna_create.html"
	form_class = DruzynaModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_success_url(self):
		return reverse("druzyny_management", kwargs={'pk':self.kwargs['pk']})
		return super(DruzynaCreateView, self).form_valid(form)

	def get_initial(self, *args, **kwargs):
		initial = super(DruzynaCreateView, self).get_initial()
		initial = initial.copy()
		initial['administrator'] = self.request.user
		initial['turniej'] = nazwa_turnieju(self.kwargs['pk'])[0].id
		return initial

	def dispatch(self, request, *args, **kwargs):
		try:
			if nazwa_turnieju(self.kwargs["pk"])[0].turniej_druzynowy and Druzyna.objects.filter(slug=self.kwargs["druzyna_slug"], administrator=self.request.user).count() > 0:
				return super(DruzynaCreateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			# return redirect("not_authorized")
			return super(DruzynaCreateView, self).dispatch(request, *args, **kwargs)