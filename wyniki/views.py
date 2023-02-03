from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, reverse
from wyniki.models import Wyniki, WynikiDynamic
from zawody.models import Sedzia, Zawody, ZawodyDynamic, SedziaDynamic, Druzyna
from account.models import Account
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from . import forms
from django.contrib.auth.decorators import login_required
import datetime
import xlwt
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .forms import WynikiModelForm, RejestracjaModelForm, TurniejModelForm, ModuleFormSet, ModuleFormSetDynamic, RejestracjaDynamicModelForm, WynikiDynamicModelForm, RejestracjaModelFormNew, RejestracjaCheckboxForm
from zawody.models import Turniej
from mainapp.views import nazwa_turnieju
from django.db.models import Count, Sum



@csrf_exempt
@login_required(login_url="/start/")
def wyniki_edycja(request, pk):
	if request.user.is_sedzia:
		context = {}
		context['pk'] = pk
		context['nazwa_turnieju'] = nazwa_turnieju(pk)
		turniej = Turniej.objects.filter(id=pk).values_list('id', flat=True)
		turniej_id = turniej[0]

		#sprawdzam konkurencje przypisane do turnieju
		zawody_turnieju = Zawody.objects.filter(turniej=turniej_id).values_list('id', flat=True)
		zawody_turnieju_id = []
		for i in zawody_turnieju:
			zawody_turnieju_id.append(i)

		#sprawdzamy użytkownika ktory jest zalogowany
		user_id = request.user.id 					
		#sprawdzamy do jakich zawodow jest przyporzadkowany zalogowany user															
		powiazane_zawody = Sedzia.objects.filter(sedzia__id = user_id).values_list('zawody', flat=True)			
		powiazane_zawody_lista = []																				
		for i in powiazane_zawody:
			if i in zawody_turnieju_id:
				powiazane_zawody_lista.append(i)

		#zapisujemy w liście wyniki wyniki wszystkich zawodników dla poszczególnych zawodów
		powiazane_zawody_lista.sort()
		wyniki = []																			
		for i in powiazane_zawody_lista:
			wynik = Wyniki.objects.filter(zawody = i).order_by('zawodnik__nazwisko')
			#do listy wyniki mają trafiać tylko te wyniki, które dotyczą konkretnego turnieju
			#gdyby nie było dodatkowego filtrowania pojawiały by się błędy w przypadku gdy jedna konkurencja występowałaby w wielu turniejach
			wyniki.append(wynik.filter(zawody__turniej=pk, oplata=1))

		#zapisujemy w liście zawody_nazwa nazwy zawodów, z którymi powiązany jest sędzia
		zawody_nazwa = []
		nazwy_zawodow = Zawody.objects.filter(id__in=powiazane_zawody_lista).values_list('nazwa', flat=True)
		#do listy zawody_nazwa mają trafiać tylko te wyniki, które dotyczą konkretnego turnieju
		#gdyby nie było dodatkowego filtrowania pojawiały by się błędy w przypadku gdy jedna konkurencja występowałaby w wielu turniejach
		nazwy_zawodow = nazwy_zawodow.filter(turniej=pk)
		for i in nazwy_zawodow:
			zawody_nazwa.append(i)
		context['wyniki'] = wyniki
		context['zawody_nazwa'] = zawody_nazwa
		
		return render(request, 'wyniki/edytuj_wyniki.html', context)
	else:
		return redirect('not_authorized')


@login_required(login_url="/start/")
def wyniki_dynamic_edycja(request, pk):
	if request.user.is_sedzia:
		context = {}
		context['pk'] = pk
		context['nazwa_turnieju'] = nazwa_turnieju(pk)
		turniej = Turniej.objects.filter(id=pk).values_list('id', flat=True)
		turniej_id = turniej[0]

		#sprawdzam konkurencje przypisane do turnieju
		zawody_turnieju = ZawodyDynamic.objects.filter(turniej=turniej_id).values_list('id', flat=True)
		zawody_turnieju_id = []
		for i in zawody_turnieju:
			zawody_turnieju_id.append(i)

		#sprawdzamy użytkownika ktory jest zalogowany
		user_id = request.user.id 					
		#sprawdzamy do jakich zawodow jest przyporzadkowany zalogowany user															
		powiazane_zawody = SedziaDynamic.objects.filter(sedzia__id = user_id).values_list('zawody', flat=True)			
		powiazane_zawody_lista = []																				
		for i in powiazane_zawody:
			if i in zawody_turnieju_id:
				powiazane_zawody_lista.append(i)

		#zapisujemy w liście wyniki wyniki wszystkich zawodników dla poszczególnych zawodów
		powiazane_zawody_lista.sort()
		wyniki = []																			
		for i in powiazane_zawody_lista:
			wynik = WynikiDynamic.objects.filter(zawody = i).order_by('zawodnik__nazwisko')
			#do listy wyniki mają trafiać tylko te wyniki, które dotyczą konkretnego turnieju
			#gdyby nie było dodatkowego filtrowania pojawiały by się błędy w przypadku gdy jedna konkurencja występowałaby w wielu turniejach
			wyniki.append(wynik.filter(zawody__turniej=pk, oplata=1))

		#zapisujemy w liście zawody_nazwa nazwy zawodów, z którymi powiązany jest sędzia
		zawody_nazwa = []
		nazwy_zawodow = ZawodyDynamic.objects.filter(id__in=powiazane_zawody_lista).values_list('nazwa', flat=True)
		#do listy zawody_nazwa mają trafiać tylko te wyniki, które dotyczą konkretnego turnieju
		#gdyby nie było dodatkowego filtrowania pojawiały by się błędy w przypadku gdy jedna konkurencja występowałaby w wielu turniejach
		nazwy_zawodow = nazwy_zawodow.filter(turniej=pk)
		for i in nazwy_zawodow:
			zawody_nazwa.append(i)
		context['wyniki'] = wyniki
		context['zawody_nazwa'] = zawody_nazwa
		
		return render(request, 'wyniki/edytuj_wyniki_dynamic.html', context)
	else:
		return redirect('not_authorized')

@login_required(login_url="/start/")
def wyniki(request, pk):
	context = {}
	context['nazwa_turnieju'] = nazwa_turnieju(pk)
	context['pk'] = pk
	klasyfikacja_generalna_display = Turniej.objects.filter(id=pk).values_list('klasyfikacja_generalna', flat=True)
	context['klasyfikacja_generalna_display'] = klasyfikacja_generalna_display[0]
	klasyfikacja_generalna = Wyniki.objects.raw('select wyniki_wyniki.id, zawodnik_id, sum(X) as X, sum(Xx) as Xx,sum(dziewiec) as dziewiec, sum(osiem) as osiem,sum(siedem) as siedem , sum(szesc) as szesc, sum(piec) as piec, sum(cztery) as cztery, sum(trzy) as trzy, sum(dwa) as dwa, sum(jeden) as jeden, sum(wynik) as wynik from wyniki_wyniki inner join zawody_zawody on wyniki_wyniki.zawody_id = zawody_zawody.id where zawody_zawody.turniej_id = %s and oplata=1 and wyniki_wyniki.kara = %s group by zawodnik_id order by wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC, szesc desc, piec desc, cztery desc, trzy desc, dwa desc, jeden desc', [pk, 'BRAK'])
	context['klasyfikacja_generalna'] = klasyfikacja_generalna

	if context['nazwa_turnieju'][0].wyniki_widoczne or request.user.rts:

		static_list = []
		zawody_static = Zawody.objects.filter(turniej__id=pk).values_list('id', flat=True).order_by('id')
		
		for i in zawody_static:
			slownik = {}
			slownik['zawody_nazwa'] = Zawody.objects.filter(id=i).values_list('nazwa', flat=True)
			slownik['wyniki'] = Wyniki.objects.filter(zawody = i, oplata=1).order_by('kara', '-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem', '-szesc', '-piec', '-cztery', '-trzy', '-dwa', '-jeden')
			slownik['sedzia'] = Sedzia.objects.filter(zawody = i).values_list('sedzia__imie', 'sedzia__nazwisko')

			static_list.append(slownik)
		context['static_list'] = static_list


		dynamic_list = []
		zawody_dynamic = ZawodyDynamic.objects.filter(turniej__id=pk).values_list('id', flat=True).order_by('id')
		
		for i in zawody_dynamic:
			slownik = {}
			slownik['zawody_nazwa'] = ZawodyDynamic.objects.filter(id=i).values_list('nazwa', flat=True)
			slownik['wyniki'] = WynikiDynamic.objects.filter(zawody = i, oplata=1).order_by('kara', 'wynik', 'czas')
			slownik['sedzia'] = SedziaDynamic.objects.filter(zawody = i).values_list('sedzia__imie', 'sedzia__nazwisko')

			dynamic_list.append(slownik)
		context['dynamic_list'] = dynamic_list

		return render(request, 'wyniki/wyniki.html', context)

	else:
		return redirect('not_authorized')


@login_required(login_url="/start/")
def wyniki_general(request, pk):
	context = {}
	context['nazwa_turnieju'] = nazwa_turnieju(pk)
	context['pk'] = pk


	if context['nazwa_turnieju'][0].wyniki_generalne_widoczne or request.user.rts:

		grupy_zawodow_w_tym_turnieju = Zawody.objects.filter(turniej__id=pk, zawody_grupa__isnull=False).values_list('zawody_grupa__nazwa', flat=True)
		# print(f'grupy_zawodow_w_tym_turnieju: {grupy_zawodow_w_tym_turnieju}')
		# for i in grupy_zawodow_w_tym_turnieju:
		# 	print(f'i: {i}')
		zawody_grup = {}
		for i in grupy_zawodow_w_tym_turnieju:
			zawody_grup[i] = Zawody.objects.filter(zawody_grupa__nazwa=i).values_list('id', flat=True)

		zawody_grup_nazwy = zawody_grup



		
		wszystkie_id_zawodow = []
		
		for j in zawody_grup:
			konkurencja_id = []
			for i in zawody_grup[j]:
				konkurencja_id.append(i)
				wszystkie_id_zawodow.append(i)
			zawody_grup[j] = konkurencja_id


		converted_list = [str(element) for element in wszystkie_id_zawodow]
		joined_wszystkie_id_zawodow = ','.join(converted_list)

		for i in zawody_grup:
			converted_list = [str(element) for element in zawody_grup[i]]
			joined_string = ",".join(converted_list)
			# print(f'joined string: {joined_string}')
			# print(f'joined string type: {type(joined_string)}')
			# print(f'zawody_grup: {zawody_grup}')
			# print(f'i: {i}')

			elements = zawody_grup[i]
			# print(f'elements: {elements}')

			select_strings_to_add = []
			display_headings = []
			from_strings_to_add = []

			for num, j in enumerate(elements):
				# print(f'num: {num}')
				select_strings_to_add.append(f'coalesce(w{j}.wynik,"Nie startował") w{num}')
				if context['nazwa_turnieju'][0].turniej_druzynowy:
					display_headings.append(f'{Zawody.objects.filter(id=j).values_list("nazwa", flat=True)[0]}')
				else:
					display_headings.append(f'{Zawody.objects.filter(id=j).values_list("turniej__nazwa", flat=True)[0]}')
				from_strings_to_add.append(f" left join (select wynik, zawodnik_id from wyniki_wyniki where wyniki_wyniki.zawody_id = {j}) w{j} on w{j}.zawodnik_id = account_account.id")

			select_converted = [str(element) for element in select_strings_to_add]
			select_string = ",".join(select_converted)

			from_converted = [str(element) for element in from_strings_to_add]
			from_string = " ".join(from_converted)






			my_string = "sum(wyniki_wyniki.osiem) as osiem, "

			# wynik_grupowy = Wyniki.objects.raw(f'select wyniki_wyniki.id, zawodnik_id from wyniki_wyniki inner join zawody_zawody on wyniki_wyniki.zawody_id = zawody_zawody.id where zawody_zawody.id in ({joined_string})')
			sql_string = "select wyniki_wyniki.id, account_account.nazwisko, account_account.imie,"\
			f"account_account.email, sum(wyniki_wyniki.X) as X, sum(wyniki_wyniki.Xx) as dziesiec, sum(wyniki_wyniki.dziewiec) as dziewiec,"\
			f"sum(wyniki_wyniki.osiem) as osiem, "\
			f"sum(wyniki_wyniki.siedem) as siedem, sum(wyniki_wyniki.szesc) as szesc, sum(wyniki_wyniki.piec) as piec, sum(wyniki_wyniki.cztery) as cztery,"\
			f"sum(wyniki_wyniki.trzy) as trzy, sum(wyniki_wyniki.dwa) as dwa, sum(wyniki_wyniki.jeden) as jeden, " \
			" case count(wyniki_wyniki.wynik) when 4 then sum(wyniki_wyniki.wynik) - min(wyniki_wyniki.wynik) else  sum(wyniki_wyniki.wynik) end Wynik," \
			f" {select_string} "\
			"from account_account "\
			"left join wyniki_wyniki on account_account.id = wyniki_wyniki.zawodnik_id "\
			f"left join zawody_zawody on zawody_zawody.id = wyniki_wyniki.zawody_id "\
			f"{from_string} "\
			f"where zawody_zawody.id in ({joined_string}) "\
			"group by account_account.id "\
			"order by Wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC, szesc desc, piec desc, cztery desc, trzy desc, dwa desc, jeden desc"
			# print(f'sql string : {sql_string}')

			wynik_grupowy = Wyniki.objects.raw(sql_string)
			zawody_grup[i] = {'wynik':wynik_grupowy, 'dupa':display_headings}
		# print(f'wszystkie_id_zawodow: {wszystkie_id_zawodow}')
		# print(f'joined_wszystkie_id_zawodow: {joined_wszystkie_id_zawodow}')
		context['wynik_grupowy'] = zawody_grup
		# print(f'zawody_grup: {zawody_grup}')
		# wynik_general = Wyniki.objects.raw(f'select wyniki_wyniki.id, account_account.nazwisko, account_account.imie, account_account.email, sum(wyniki_wyniki.X) as X, sum(wyniki_wyniki.Xx) as dziesiec, sum(wyniki_wyniki.dziewiec) as dziewiec, sum(wyniki_wyniki.osiem) as osiem, sum(wyniki_wyniki.siedem) as siedem, sum(wyniki_wyniki.szesc) as szesc, sum(wyniki_wyniki.piec) as piec, sum(wyniki_wyniki.cztery) as cztery, sum(wyniki_wyniki.trzy) as trzy, sum(wyniki_wyniki.dwa) as dwa, sum(wyniki_wyniki.jeden) as jeden, sum(wyniki_wyniki.X*10 + wyniki_wyniki.Xx*10 + wyniki_wyniki.dziewiec*9 + wyniki_wyniki.osiem*8 + wyniki_wyniki.siedem*7 + wyniki_wyniki.szesc*6 + wyniki_wyniki.piec*5 + wyniki_wyniki.cztery*4 + wyniki_wyniki.trzy*3 + wyniki_wyniki.dwa*2 + wyniki_wyniki.jeden*1) as Wynik from account_account left join wyniki_wyniki on account_account.id = wyniki_wyniki.zawodnik_id left join zawody_zawody on zawody_zawody.id = wyniki_wyniki.zawody_id where zawody_zawody.id in ({joined_wszystkie_id_zawodow}) group by account_account.id order by Wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC, szesc desc, piec desc, cztery desc, trzy desc, dwa desc, jeden desc')
		# context['wynik_general'] = wynik_general

		# print(f'dict: {zawody_grup}')

		turniej_grup = []

		for i in grupy_zawodow_w_tym_turnieju:
			turniej_grup.append(Zawody.objects.filter(zawody_grupa__nazwa=i).values_list('turniej_id', flat=True))


		turniej_grup_flat = []
		for i in turniej_grup:
			for j in i:
				turniej_grup_flat.append(j)

		turniej_grup_set = sorted(set(turniej_grup_flat))

		
		# print(f'turniej_grup: {turniej_grup}')
		# print(f'turniej_grup_set: {turniej_grup_set}')
		# print(f'zawody_grup_flat: {zawody_grup_flat}')
		for i in turniej_grup_set:
			converted_list = [str(element) for element in turniej_grup_set]
			joined_string_turnieje = ",".join(converted_list)
		# print(f'joined_string_turnieje: {joined_string_turnieje}')

################################################



			# elements = zawody_grup[i]
			# print(f'elements: {elements}')

		select_strings_general = []
		display_headings_general = []
		from_strings_general = []

		for num, j in enumerate(turniej_grup_set):
				# print(f'num: {num}')
			select_strings_general.append(f'coalesce(w{j}.wynik,"Nie startował") w{num}')
			# if context['nazwa_turnieju'][0].turniej_druzynowy:
			# 	display_headings_general.append(f'{Zawody.objects.filter(id=j).values_list("nazwa", flat=True)[0]}')
			# else:
			# 	display_headings_general.append(f'{Turniej.objects.filter(id=j).values_list("nazwa", flat=True)[0]}')
			display_headings_general.append(f'{Turniej.objects.filter(id=j).values_list("nazwa", flat=True)[0]}')
			from_strings_general.append(f" left join (select sum(wyniki_wyniki.wynik) wynik, zawodnik_id from wyniki_wyniki join zawody_zawody on wyniki_wyniki.zawody_id = zawody_zawody.id where zawody_zawody.turniej_id={j} group by wyniki_wyniki.zawodnik_id) w{j} on w{j}.zawodnik_id = account_account.id")

		select_converted = [str(element) for element in select_strings_general]
		select_string_general = ",".join(select_converted)

		from_converted = [str(element) for element in from_strings_general]
		from_strings_general = " ".join(from_converted)

################################################

		sql_string = "select account_account.id id, "\
					"account_account.nazwisko, "\
					"account_account.nazwisko||' '||account_account.imie zawodnik, "\
					"account_account.email, "\
					"case count(wall.wynik) when 4 then sum(wall.wynik) - min(wall.wynik) else  sum(wall.wynik) end Wynik, "\
					f"{select_string_general} "\
					"from account_account "\
					f"{from_strings_general} "\
					f"left join (select sum(wyniki_wyniki.wynik) wynik, zawody_turniej.id turniej_id, zawodnik_id from wyniki_wyniki join zawody_zawody on wyniki_wyniki.zawody_id = zawody_zawody.id join zawody_turniej on zawody_turniej.id = zawody_zawody.turniej_id where zawody_turniej.id in ({joined_string_turnieje}) group by wyniki_wyniki.zawodnik_id, zawody_turniej.id) wall on wall.zawodnik_id = account_account.id "\
					"group by account_account.id "\
					"order by Wynik desc "\

		# print(f'sql string: {sql_string}')

		wynik_generalny_sql = Account.objects.raw(sql_string)
		wynik_generalny = {'wynik':wynik_generalny_sql, 'header':display_headings}
		context['wynik_generalny'] = wynik_generalny

#######################################









		return render(request, 'wyniki/wyniki_general.html', context)

	else:
		return redirect('not_authorized')




@login_required(login_url="/start/")
def wyniki_druzynowe(request, pk):
	context = {}
	context['nazwa_turnieju'] = nazwa_turnieju(pk)
	context['pk'] = pk


	if context['nazwa_turnieju'][0].turniej_druzynowy or request.user.rts:

		zawody_w_tym_turnieju = Zawody.objects.filter(turniej__id=pk)

		
		wyniki = []
		for i in zawody_w_tym_turnieju:
			wyniki.append({'nazwa':i.nazwa, 'id':i.id})
# 		print(f'wyniki: {wyniki}')



		for i in wyniki:
			where_string = str(i["id"])
			sql_string = "select zawody_druzyna.id, zawody_druzyna.nazwa,"\
			"group_concat(account_account.nazwisko||' '||account_account.imie, char(10)) team,"\
			"sum(wyniki_wyniki.wynik) Wynik "\
			"from zawody_druzyna "\
			"join zawody_zawodnicydruzyny on zawody_druzyna.id = zawody_zawodnicydruzyny.druzyna_id "\
			"join account_account on account_account.id = zawody_zawodnicydruzyny.zawodnik_id "\
			"join zawody_turniej on zawody_turniej.id = zawody_druzyna.turniej_id "\
			"join zawody_zawody on zawody_zawody.turniej_id = zawody_turniej.id "\
			"join wyniki_wyniki on wyniki_wyniki.zawody_id = zawody_zawody.id and wyniki_wyniki.zawodnik_id = zawody_zawodnicydruzyny.zawodnik_id "\
			f"where zawody_zawody.id = {where_string} "\
			"group by zawody_druzyna.nazwa "\
			"order by Wynik desc"

			wyniki_konkurencji = Druzyna.objects.raw(sql_string)

			i['wyniki_konkurencji']=wyniki_konkurencji


		context['wyniki'] = wyniki


		turniej_id_string = str(pk)

		sql_string_summary = "select zawody_druzyna.id id, zawody_druzyna.nazwa,"\
		"replace(group_concat(distinct cte.zawodnik), ',', char(10)) team,"\
		"sum(wyniki_wyniki.wynik) Wynik "\
		"from wyniki_wyniki "\
		"join zawody_zawody on zawody_zawody.id = wyniki_wyniki.zawody_id "\
		"join zawody_turniej on zawody_turniej.id = zawody_zawody.turniej_id "\
		"join zawody_druzyna on zawody_druzyna.turniej_id = zawody_turniej.id "\
		"join zawody_zawodnicydruzyny on zawody_druzyna.id = zawody_zawodnicydruzyny.druzyna_id "\
		"join account_account on account_account.id = zawody_zawodnicydruzyny.zawodnik_id and wyniki_wyniki.zawodnik_id = account_account.id "\
		"join (select (usr.nazwisko||' '||usr.imie) zawodnik, usr.id usid from account_account usr) cte on cte.usid = account_account.id "\
		f"where zawody_turniej.id = {turniej_id_string} "\
		"group by zawody_druzyna.nazwa "\
		"order by Wynik desc"\

		wyniki_koncowe = Druzyna.objects.raw(sql_string_summary)

		context['wyniki_koncowe'] = wyniki_koncowe


	

		# print(f'dict: {zawody_grup}')
		return render(request, 'wyniki/wyniki_druzynowe.html', context)

	else:
		return redirect('not_authorized')



@login_required(login_url="/start/")
def rejestracja_choose(request, pk):
	context = {}
	context['nazwa_turnieju'] = nazwa_turnieju(pk)
	context['pk'] = pk

	# print(f'dict: {zawody_grup}')
	return render(request, 'wyniki/rejestracja_choose.html', context)






class RejestracjaNaZawodyView(LoginRequiredMixin, CreateView):
	login_url = 'start'
	template_name = "wyniki/rejestracja.html"
	form_class = RejestracjaModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		#sprawdzam czy rejestracja jest otwarta i podaję informację o tym w argumencie 'dodawanie_zawodnika'
		dodawanie_zawodnika = Turniej.objects.filter(id=self.kwargs['pk']).values_list("rejestracja", flat=True)
		rejestracja_otwarta = dodawanie_zawodnika[0]
		context['dodawanie_zawodnika'] = rejestracja_otwarta
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		# lista_zarejestrowanych = Wyniki.objects.filter(zawodnik__id = self.request.user.id).filter(zawody__turniej__id = self.kwargs['pk']).values_list("zawody__nazwa", flat=True)
		lista_zarejestrowanych = Wyniki.objects.filter(zawodnik__id = self.request.user.id).filter(zawody__turniej__id = self.kwargs['pk'])
		context['lista_zarejestrowanych'] = lista_zarejestrowanych
		suma_oplat = 0
		for i in lista_zarejestrowanych:
			suma_oplat += i.zawody.oplata_konkurencja
			if i.amunicja_klubowa:
				suma_oplat += i.zawody.oplata_amunicja
			if i.bron_klubowa:
				suma_oplat += i.zawody.oplata_bron

			# print(f'konkurencja: {i.zawody} amunicja_klubowa: {i.amunicja_klubowa}  cena: {i.zawody.oplata_amunicja}')
			# print(f'konkurencja: {i.zawody} broń klubowa: {i.bron_klubowa} cena: {i.zawody.oplata_bron} ')
		context['suma_oplat'] = suma_oplat
		return context

	def get_success_url(self):
		return reverse("rejestracja_na_zawody", kwargs={'pk': self.kwargs['pk']})
		return super(RejestracjaNaZawodyView, self).form_valid(form)

	def get_form_kwargs(self):
		kwargs = super(RejestracjaNaZawodyView, self).get_form_kwargs()
		kwargs.update({'user': self.request.user.rts})
		kwargs.update({'pk': self.kwargs['pk']})
		return kwargs

	def get_initial(self, *args, **kwargs):
		initial = super(RejestracjaNaZawodyView, self).get_initial()
		initial = initial.copy()
		initial['zawodnik'] = self.request.user
		return initial


@csrf_exempt
@login_required(login_url="")
def rejestracja_na_zawody_checkbox(request, pk):

	context={}
	context['pk'] = pk
	context['nazwa_turnieju'] = nazwa_turnieju(pk)

		
	if request.method == 'POST':
		print('post')

		form = RejestracjaCheckboxForm(request.POST, zawody_pk=pk)
			# print(form)
		print(form.errors)
			# print(form.cleaned_data.get('zawody'))
		if form.is_valid():

			zawody = form.cleaned_data.get('zawody')
			zawodnik = form.cleaned_data.get('Zawodnik')
			print(f'zawody: {zawody}')
			print(f'sedzia: {sedzia}')

			for i in zawody:
				zaw = Zawody.objects.filter(id=i)[0]
				for j in sedzia:
					zawodn = Account.objects.filter(id=j)[0]
					if not Wyniki.objects.filter(zawody__id=i, zawodnik__id=j):
						Wyniki.objects.create(zawody=zaw , zawodnik=zawodn)



		form = RejestracjaCheckboxForm(zawody_pk=pk)
	else:
		form = RejestracjaCheckboxForm(zawody_pk=pk)

	context['form'] = form

	return render(request, 'wyniki/rejestracja_checkbox.html', context)



def rejestracja_na_zawody(request, pk):
	context={}
	context['pk'] = pk
	context['nazwa_turnieju'] = nazwa_turnieju(pk)
	lista_zarejestrowanych = Wyniki.objects.filter(zawodnik__id = request.user.id).filter(zawody__turniej__id = pk)
	context['lista_zarejestrowanych'] = lista_zarejestrowanych


	dodawanie_zawodnika = Turniej.objects.filter(id=pk).values_list("rejestracja", flat=True)
	rejestracja_otwarta = dodawanie_zawodnika[0]
	context['dodawanie_zawodnika'] = rejestracja_otwarta
	for i in lista_zarejestrowanych:
		suma_oplat += i.zawody.oplata_konkurencja
		if i.amunicja_klubowa:
			suma_oplat += i.zawody.oplata_amunicja
		if i.bron_klubowa:
			suma_oplat += i.zawody.oplata_bron

			# print(f'konkurencja: {i.zawody} amunicja_klubowa: {i.amunicja_klubowa}  cena: {i.zawody.oplata_amunicja}')
			# print(f'konkurencja: {i.zawody} broń klubowa: {i.bron_klubowa} cena: {i.zawody.oplata_bron} ')
	# context['suma_oplat'] = suma_oplat
	
	if request.method == 'POST':
		form = RejestracjaModelFormNew(request.POST)
		if form.is_valid():
			pass
	else:
		form = RejestracjaModelFormNew(user=request.user, pk=pk, initial={'zawodnik': request.user.id})

	context['form'] = form

	return render(request, 'wyniki/rejestracja.html', context)





class RejestracjaNaZawodyDynamicView(LoginRequiredMixin, CreateView):
	login_url = 'start'
	template_name = "wyniki/rejestracja_dynamic.html"
	form_class = RejestracjaDynamicModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		#sprawdzam czy rejestracja jest otwarta i podaję informację o tym w argumencie 'dodawanie_zawodnika'
		dodawanie_zawodnika = Turniej.objects.filter(id=self.kwargs['pk']).values_list("rejestracja", flat=True)
		rejestracja_otwarta = dodawanie_zawodnika[0]
		context['dodawanie_zawodnika'] = rejestracja_otwarta
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		# lista_zarejestrowanych = Wyniki.objects.filter(zawodnik__id = self.request.user.id).filter(zawody__turniej__id = self.kwargs['pk']).values_list("zawody__nazwa", flat=True)
		lista_zarejestrowanych = WynikiDynamic.objects.filter(zawodnik__id = self.request.user.id).filter(zawody__turniej__id = self.kwargs['pk'])
		context['lista_zarejestrowanych'] = lista_zarejestrowanych
		suma_oplat = 0
		for i in lista_zarejestrowanych:
			suma_oplat += i.zawody.oplata_konkurencja
			if i.amunicja_klubowa:
				suma_oplat += i.zawody.oplata_amunicja
			if i.bron_klubowa:
				suma_oplat += i.zawody.oplata_bron

			# print(f'konkurencja: {i.zawody} amunicja_klubowa: {i.amunicja_klubowa}  cena: {i.zawody.oplata_amunicja}')
			# print(f'konkurencja: {i.zawody} broń klubowa: {i.bron_klubowa} cena: {i.zawody.oplata_bron} ')
		context['suma_oplat'] = suma_oplat
		return context

	def get_success_url(self):
		return reverse("rejestracja_na_zawody_dynamic", kwargs={'pk': self.kwargs['pk']})
		return super(RejestracjaNaZawodyDynamicView, self).form_valid(form)

	def get_form_kwargs(self):
		kwargs = super(RejestracjaNaZawodyDynamicView, self).get_form_kwargs()
		kwargs.update({'user': self.request.user.rts})
		kwargs.update({'pk': self.kwargs['pk']})
		return kwargs

	def get_initial(self, *args, **kwargs):
		initial = super(RejestracjaNaZawodyDynamicView, self).get_initial()
		initial = initial.copy()
		initial['zawodnik'] = self.request.user
		return initial


class WynikUpdateView(LoginRequiredMixin, UpdateView):
	login_url = 'start'
	template_name = "wyniki/wyniki_edit.html"
	form_class = WynikiModelForm
	context_object_name = 'cont'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		return context

	def get_queryset(self):
		return Wyniki.objects.all()

	def get_success_url(self):
		return reverse("wyniki_edycja", kwargs={'pk': self.kwargs['pk_turniej']})

	def form_valid(self, form):
		return super(WynikUpdateView,self).form_valid(form)

	def get_form_kwargs(self):
		kwargs = super(WynikUpdateView, self).get_form_kwargs()
		zawody = Wyniki.objects.filter(id = self.kwargs['pk']).values_list('zawody__id', flat=True)
		# print(f'zawody: {zawody[0]}')
		liczba_strzalow = Zawody.objects.filter(id = zawody[0]).values_list('liczba_strzalow', flat=True)
		liczba_strzalow_range = list(range(0,liczba_strzalow[0]+1))
		lista = []
		for i in liczba_strzalow_range:
			lista.append(tuple((i,i)))
		kwargs.update({'strzaly': lista})
		# kwargs.update({'is_sedzia_editing': self.request.user.is_sedzia and not self.request.user.rts})
		return kwargs


	def dispatch(self, request, *args, **kwargs):
		wynik_pk = self.kwargs.get('pk')
		wynik_edytowany = Wyniki.objects.filter(id = wynik_pk).values_list('edited_by_sedzia', flat=True)
		zawody_pk = Wyniki.objects.filter(id = wynik_pk).values_list('zawody__id', flat=True)
		zawody_pk_lista = []
		for i in zawody_pk:
			zawody_pk_lista.append(i)
		zawody_pk_lista = zawody_pk_lista[0]
		sedzia_pk = Sedzia.objects.filter(zawody__id = zawody_pk_lista).values_list('sedzia__id', flat=True)
		sedzia_pk_lista = []
		for i in sedzia_pk:
			sedzia_pk_lista.append(i)
		user_id=self.request.user.id
		sedzia_not_rts = self.request.user.is_sedzia and not self.request.user.rts
		if user_id in sedzia_pk_lista:
			if sedzia_not_rts and wynik_edytowany[0]:
				return redirect('not_authorized')
			else:
				return super(WynikUpdateView, self).dispatch(request, *args, **kwargs)
		else:
			return redirect('not_authorized')


class WynikDynamicUpdateView(LoginRequiredMixin, UpdateView):
	login_url = 'start'
	template_name = "wyniki/wyniki_dynamic_edit.html"
	form_class = WynikiDynamicModelForm
	context_object_name = 'cont'






	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		zawody = WynikiDynamic.objects.filter(id = self.kwargs['pk']).values_list('zawody__id', flat=True)
		miss = ZawodyDynamic.objects.filter(id = zawody[0]).values_list('miss', flat=True)
		procedura = ZawodyDynamic.objects.filter(id = zawody[0]).values_list('procedura', flat=True)
		noshoot = ZawodyDynamic.objects.filter(id = zawody[0]).values_list('noshoot', flat=True)
		context['miss'] = miss[0]
		context['procedura'] = procedura[0]
		context['noshoot'] = noshoot[0]
		return context

	def get_queryset(self):
		return WynikiDynamic.objects.all()

	def get_success_url(self):
		return reverse("wyniki_dynamic_edycja", kwargs={'pk': self.kwargs['pk_turniej']})

	def form_valid(self, form):
		return super(WynikDynamicUpdateView,self).form_valid(form)

	def get_form_kwargs(self):
		kwargs = super(WynikDynamicUpdateView, self).get_form_kwargs()
		zawody = WynikiDynamic.objects.filter(id = self.kwargs['pk']).values_list('zawody__id', flat=True)
		# print(f'zawody: {zawody[0]}')
		miss = ZawodyDynamic.objects.filter(id = zawody[0]).values_list('miss', flat=True)
		procedura = ZawodyDynamic.objects.filter(id = zawody[0]).values_list('procedura', flat=True)
		noshoot = ZawodyDynamic.objects.filter(id = zawody[0]).values_list('noshoot', flat=True)



		return kwargs


	def dispatch(self, request, *args, **kwargs):
		wynik_pk = self.kwargs.get('pk')
		wynik_edytowany = WynikiDynamic.objects.filter(id = wynik_pk).values_list('edited_by_sedzia', flat=True)
		zawody_pk = WynikiDynamic.objects.filter(id = wynik_pk).values_list('zawody__id', flat=True)
		zawody_pk_lista = []
		for i in zawody_pk:
			zawody_pk_lista.append(i)
		zawody_pk_lista = zawody_pk_lista[0]
		sedzia_pk = SedziaDynamic.objects.filter(zawody__id = zawody_pk_lista).values_list('sedzia__id', flat=True)
		sedzia_pk_lista = []
		for i in sedzia_pk:
			sedzia_pk_lista.append(i)
		user_id=self.request.user.id
		sedzia_not_rts = self.request.user.is_sedzia and not self.request.user.rts
		if user_id in sedzia_pk_lista:
			if sedzia_not_rts and wynik_edytowany[0]:
				return redirect('not_authorized')
			else:
				return super(WynikDynamicUpdateView, self).dispatch(request, *args, **kwargs)
		else:
			return redirect('not_authorized')


def not_authorized(request):
	return render(request, 'wyniki/not_authorized.html')

@login_required(login_url="/start/")
def exportexcel(request, pk):
	if request.user.is_admin:
		response=HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename=Wyniki_' + str(datetime.datetime.now())+'.xls'
		wb = xlwt.Workbook(encoding='utf-8')

		zawody = Zawody.objects.filter(turniej__id=pk).values_list('nazwa', flat=True).order_by('id')
		ws = []
		for i in zawody:
			ws.append(wb.add_sheet(i))

		row_num = 0
		font_style = xlwt.XFStyle()
		font_style.font.bold=True

		columns = ['Pozycja','Nazwisko','Imię', 'Klub', 'Suma']

		for col_num in range(len(columns)):
			for i in ws:
				i.write(row_num, col_num, columns[col_num], font_style)


		font_style = xlwt.XFStyle()
		zawody_id = Zawody.objects.filter(turniej__id=pk).values_list('id', flat=True).order_by('id')
		zawody_id_lista = []
		for i in zawody_id:
			zawody_id_lista.append(i)


		rows = []
		for count, i in enumerate(zawody_id_lista):
			rows.append(Wyniki.objects.filter(zawody__id = i, oplata = 1).values_list('zawodnik__nazwisko','zawodnik__imie', 'zawodnik__klub', 'result','wynik', 'X', 'Xx', 'dziewiec', 'osiem', 'siedem', 'szesc', 'piec', 'cztery', 'trzy', 'dwa', 'jeden', 'kara').order_by('kara', '-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem', '-szesc', '-piec', '-cztery', '-trzy', '-dwa', '-jeden'))
			# queryset = Wyniki.objects.filter(zawody__id = i, oplata = 1).values_list('zawodnik__nazwisko','zawodnik__imie', 'zawodnik__klub', 'wynik').order_by('-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem', '-szesc', '-piec', '-cztery', '-trzy', '-dwa', '-jeden')
			# items = zip(range(1,queryset.count()+1), queryset)


			# rows.append(items)

		# rows.append(Wyniki.objects.filter(zawody__turniej = pk, oplata = 1).values_list('zawodnik__nazwisko','zawodnik__imie', 'zawodnik__klub', 'X', 'Xx', 'dziewiec', 'osiem', 'siedem', 'szesc', 'piec', 'cztery', 'trzy', 'dwa', 'jeden', 'wynik', 'kara').order_by('-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem', '-szesc', '-piec', '-cztery', '-trzy', '-dwa', '-jeden'))	
		generalka = Wyniki.objects.raw('select account_account.nazwisko, account_account.imie, account_account.klub, sum(wynik) as wynik, sum(X) as X, sum(dziewiec) as dziewiec, sum(osiem) as osiem, sum(siedem) as siedem, sum(szesc) as szesc,  account_account.id from account_account inner join zawody_zawody on wyniki_wyniki.zawody_id = zawody_zawody.id inner join wyniki_wyniki on account_account.id=wyniki_wyniki.zawodnik_id where zawody_zawody.turniej_id = %s and oplata=1 and wyniki_wyniki.kara = %s group by account_account.id order by wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC', [pk, 'BRAK'])
		# generalka = Wyniki.objects.raw('select wyniki_wyniki.id, zawodnik_id, sum(X) as X, sum(Xx) as Xx,sum(dziewiec) as dziewiec, sum(osiem) as osiem,sum(siedem) as siedem , sum(szesc) as szesc, sum(piec) as piec, sum(cztery) as cztery, sum(trzy) as trzy, sum(dwa) as dwa, sum(jeden) as jeden, sum(wynik) as wynik from wyniki_wyniki inner join zawody_zawody on wyniki_wyniki.zawody_id = zawody_zawody.id where zawody_zawody.turniej_id = %s and oplata=1 and wyniki_wyniki.kara = %s group by zawodnik_id order by wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC', [pk, 'BRAK'])
		# rows.append(generalka)
		for x,y in enumerate(ws):
			row_num = 0
			for index, row in enumerate(rows[x], start=1):
				row_num +=1
				for col_num in range(len(columns)):
					if col_num==0:
						y.write(row_num, col_num, index, font_style)
					else:
						y.write(row_num, col_num, str(row[col_num-1]), font_style)

		klasyfikacja_generalna_display = Turniej.objects.filter(id=pk).values_list('klasyfikacja_generalna', flat=True)
		if klasyfikacja_generalna_display[0] == 1:

			ws.append(wb.add_sheet("Klasyfikacja generalna"))
			columns = ['Pozycja','Nazwisko','Imię', 'Klub', 'Suma']
			row_num = 0
			font_style = xlwt.XFStyle()
			font_style.font.bold=True
			for col_num in range(len(columns)):
					ws[len(ws)-1].write(row_num, col_num, columns[col_num], font_style)

			font_style = xlwt.XFStyle()
			tab_generalka = len(ws)-1
			for i,y in enumerate(generalka):
				ws[tab_generalka].write(i+1,   0, i+1, font_style)
				ws[tab_generalka].write(i+1, 1, y.nazwisko, font_style)
				ws[tab_generalka].write(i+1, 2, y.imie, font_style)
				ws[tab_generalka].write(i+1, 3, y.klub, font_style)
				ws[tab_generalka].write(i+1, 4, y.wynik, font_style)


		ws.append(wb.add_sheet("Sędziowie"))
		columns = ['Klasa', 'Nazwisko', 'Imię']
		row_num=0
		font_style = xlwt.XFStyle()
		font_style.font.bold=True
		tab_sedziowie = len(ws)-1

		for col_num in range(len(columns)):
			ws[tab_sedziowie].write(row_num, col_num, columns[col_num], font_style)



		font_style = xlwt.XFStyle()
		sedziowie = Sedzia.objects.filter(zawody__id__in = zawody_id_lista).values_list('sedzia__klasa_sedziego', 'sedzia__nazwisko', 'sedzia__imie').distinct()
		# print(sedziowie)
		for sedzia in sedziowie:
			row_num +=1
			for col_num in range(len(sedzia)):
				ws[tab_sedziowie].write(row_num, col_num, str(sedzia[col_num]), font_style)




		wb.save(response)

		return(response)

	else:
		return redirect('home')




@login_required(login_url="/start/")
def exportexceldynamic(request, pk):
	if request.user.is_admin:
		response=HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename=Wyniki_' + str(datetime.datetime.now())+'.xls'
		wb = xlwt.Workbook(encoding='utf-8')

		zawody = ZawodyDynamic.objects.filter(turniej__id=pk).values_list('nazwa', flat=True).order_by('id')
		ws = []
		for i in zawody:
			ws.append(wb.add_sheet(i))

		row_num = 0
		font_style = xlwt.XFStyle()
		font_style.font.bold=True

		columns = ['Pozycja','Nazwisko','Imię', 'Klub', 'Wynik']

		for col_num in range(len(columns)):
			for i in ws:
				i.write(row_num, col_num, columns[col_num], font_style)


		font_style = xlwt.XFStyle()
		zawody_id = ZawodyDynamic.objects.filter(turniej__id=pk).values_list('id', flat=True).order_by('id')
		zawody_id_lista = []
		for i in zawody_id:
			zawody_id_lista.append(i)


		rows = []
		for count, i in enumerate(zawody_id_lista):
			rows.append(WynikiDynamic.objects.filter(zawody__id = i, oplata = 1).values_list('zawodnik__nazwisko','zawodnik__imie', 'zawodnik__klub', 'wynik').order_by('kara', 'wynik', 'czas'))
			# queryset = Wyniki.objects.filter(zawody__id = i, oplata = 1).values_list('zawodnik__nazwisko','zawodnik__imie', 'zawodnik__klub', 'wynik').order_by('-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem', '-szesc', '-piec', '-cztery', '-trzy', '-dwa', '-jeden')
			# items = zip(range(1,queryset.count()+1), queryset)


			# rows.append(items)

		# rows.append(Wyniki.objects.filter(zawody__turniej = pk, oplata = 1).values_list('zawodnik__nazwisko','zawodnik__imie', 'zawodnik__klub', 'X', 'Xx', 'dziewiec', 'osiem', 'siedem', 'szesc', 'piec', 'cztery', 'trzy', 'dwa', 'jeden', 'wynik', 'kara').order_by('-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem', '-szesc', '-piec', '-cztery', '-trzy', '-dwa', '-jeden'))	
		# generalka = Wyniki.objects.raw('select account_account.nazwisko, account_account.imie, account_account.klub, sum(wynik) as wynik, account_account.id from account_account inner join zawody_zawody on wyniki_wyniki.zawody_id = zawody_zawody.id inner join wyniki_wyniki on account_account.id=wyniki_wyniki.zawodnik_id where zawody_zawody.turniej_id = %s and oplata=1 and wyniki_wyniki.kara = %s group by account_account.id order by wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC', [pk, 'BRAK'])
		# generalka = Wyniki.objects.raw('select wyniki_wyniki.id, zawodnik_id, sum(X) as X, sum(Xx) as Xx,sum(dziewiec) as dziewiec, sum(osiem) as osiem,sum(siedem) as siedem , sum(szesc) as szesc, sum(piec) as piec, sum(cztery) as cztery, sum(trzy) as trzy, sum(dwa) as dwa, sum(jeden) as jeden, sum(wynik) as wynik from wyniki_wyniki inner join zawody_zawody on wyniki_wyniki.zawody_id = zawody_zawody.id where zawody_zawody.turniej_id = %s and oplata=1 and wyniki_wyniki.kara = %s group by zawodnik_id order by wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC', [pk, 'BRAK'])
		# rows.append(generalka)
		for x,y in enumerate(ws):
			row_num = 0
			for index, row in enumerate(rows[x], start=1):
				row_num +=1
				for col_num in range(len(row)+1):
					if col_num==0:
						y.write(row_num, col_num, index, font_style)
					else:
						y.write(row_num, col_num, str(row[col_num-1]), font_style)




		ws.append(wb.add_sheet("Sędziowie"))
		columns = ['Klasa', 'Nazwisko', 'Imię']
		row_num=0
		font_style = xlwt.XFStyle()
		font_style.font.bold=True
		tab_sedziowie = len(ws)-1

		for col_num in range(len(columns)):
			ws[tab_sedziowie].write(row_num, col_num, columns[col_num], font_style)



		font_style = xlwt.XFStyle()
		sedziowie = SedziaDynamic.objects.filter(zawody__id__in = zawody_id_lista).values_list('sedzia__klasa_sedziego', 'sedzia__nazwisko', 'sedzia__imie').distinct()
		print(sedziowie)
		for sedzia in sedziowie:
			row_num +=1
			for col_num in range(len(sedzia)):
				ws[tab_sedziowie].write(row_num, col_num, str(sedzia[col_num]), font_style)




		wb.save(response)

		return(response)

	else:
		return redirect('home')


class KonkurencjaDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "wyniki/konkurencja_delete.html"
	context_object_name = 'zawodnik'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		return context

	def get_queryset(self):
		return Wyniki.objects.all()

	def get_success_url(self):
		return reverse("wyniki", kwargs={'pk': self.kwargs['pk_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.rts:
				return super(KonkurencjaDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')

class KonkurencjaDynamicDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "wyniki/konkurencja_delete.html"
	context_object_name = 'zawodnik'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		return context

	def get_queryset(self):
		return WynikiDynamic.objects.all()

	def get_success_url(self):
		return reverse("wyniki", kwargs={'pk': self.kwargs['pk_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.rts:
				return super(KonkurencjaDynamicDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')


class TurniejListView(LoginRequiredMixin, ListView):
	login_url = 'start'
	template_name = "wyniki/turniej_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_queryset(self):
		return Turniej.objects.all()

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(TurniejListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')



class TurniejDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "wyniki/turniej_delete.html"
	context_object_name = 'turniej'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		return context

	def get_queryset(self):
		return Turniej.objects.all()

	def get_success_url(self):
		return reverse("turnieje", kwargs={'pk': self.kwargs['pk_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(TurniejDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')




class TurniejCreateView(LoginRequiredMixin, CreateView):
	login_url = 'start'
	template_name = "wyniki/turniej_create.html"
	form_class = TurniejModelForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_success_url(self):
		return reverse("turnieje", kwargs={'pk':self.kwargs['pk']})
		return super(TurniejListView, self).form_valid(form)
	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(TurniejCreateView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect("not_authorized")



class TurniejEditView(LoginRequiredMixin,UpdateView):
	login_url = 'start'
	template_name = "wyniki/turniej_edit.html"
	form_class = TurniejModelForm
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		return context

	def get_queryset(self):
		return Turniej.objects.all()

	def get_success_url(self):
		return reverse("turnieje", kwargs={'pk':self.kwargs['pk_turniej']})
		return super(TurniejEditView, self).form_valid(form)

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_admin:
				return super(TurniejEditView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')


class OplataListView(LoginRequiredMixin, ListView):
	login_url = 'start'
	template_name = "wyniki/oplata_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_queryset(self):
		turniej_zawodnicy = Wyniki.objects.filter(zawody__turniej__id = self.kwargs['pk']).values_list('zawodnik__id')
		turniej_zawodnicy_id = []
		for i in turniej_zawodnicy:
			turniej_zawodnicy_id.append(i[0])
		turniej_zawodnicy_id_set = set(turniej_zawodnicy_id)
		o1 =  Account.objects.filter(id__in = turniej_zawodnicy_id_set).order_by('nazwisko')
		o2 =  Wyniki.objects.filter(zawodnik__id__in = turniej_zawodnicy_id_set, zawody__turniej__id = self.kwargs['pk']).values_list('zawodnik__id','zawodnik__email','zawody__nazwa').order_by('zawodnik__nazwisko')
		return [o1, o2]
		# return Account.objects.filter(id__in = turniej_zawodnicy_id_set).order_by('nazwisko')

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.rts or request.user.is_superuser:
				return super(OplataListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')
			# pass

class OplataDynamicListView(LoginRequiredMixin, ListView):
	login_url = 'start'
	template_name = "wyniki/oplata_dynamic_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		return context

	def get_queryset(self):
		turniej_zawodnicy = WynikiDynamic.objects.filter(zawody__turniej__id = self.kwargs['pk']).values_list('zawodnik__id')
		turniej_zawodnicy_id = []
		for i in turniej_zawodnicy:
			turniej_zawodnicy_id.append(i[0])
		turniej_zawodnicy_id_set = set(turniej_zawodnicy_id)
		o1 =  Account.objects.filter(id__in = turniej_zawodnicy_id_set).order_by('nazwisko')
		o2 =  WynikiDynamic.objects.filter(zawodnik__id__in = turniej_zawodnicy_id_set, zawody__turniej__id = self.kwargs['pk']).values_list('zawodnik__id','zawodnik__email','zawody__nazwa').order_by('zawodnik__nazwisko')
		return [o1, o2]
		# return Account.objects.filter(id__in = turniej_zawodnicy_id_set).order_by('nazwisko')

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.rts or request.user.is_superuser:
				return super(OplataDynamicListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')
			# pass




class OplataUpdateView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url='start'
    template_name = 'wyniki/oplata_update.html'
    account = None

    def get_formset(self, data=None, turniej=1):
        return ModuleFormSet(instance=self.account,queryset=Wyniki.objects.filter(zawody__turniej__id=turniej),
                             data=data)

    def dispatch(self, request, pk, pk_turniej):
    	try:

    		if request.user.rts or request.user.is_superuser:
    			self.account = get_object_or_404(Account,
		                                        id=pk)
    			return super().dispatch(request, pk)
    		else:
    			return reverse('not_authorized')
    	except:
    		return redirect(reverse('not_authorized'))


    def get(self, request, *args, **kwargs):
        formset = self.get_formset(turniej=self.kwargs['pk_turniej'])
        return self.render_to_response({'account': self.account,
                                        'formset': formset,
                                        'pk': self.kwargs['pk_turniej'],
                                        'nazwa_turnieju': nazwa_turnieju(self.kwargs['pk_turniej'])})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST, turniej=self.kwargs['pk_turniej'])
        if formset.is_valid():
            formset.save()
            return redirect(reverse("oplata_list", kwargs={'pk': self.kwargs['pk_turniej']}))
        return self.render_to_response({'account': self.account,
                                        'formset': formset,
                                        'pk': self.kwargs['pk_turniej'],
                                        'nazwa_turnieju': nazwa_turnieju(self.kwargs['pk_turniej'])})






class OplataDynamicUpdateView(LoginRequiredMixin, TemplateResponseMixin, View):
    login_url='start'
    template_name = 'wyniki/oplata_update.html'
    account = None

    def get_formset(self, data=None, turniej=1):
        return ModuleFormSetDynamic(instance=self.account,queryset=WynikiDynamic.objects.filter(zawody__turniej__id=turniej),
                             data=data)

    def dispatch(self, request, pk, pk_turniej):
    	try:

    		if request.user.rts or request.user.is_superuser:
    			self.account = get_object_or_404(Account,
		                                        id=pk)
    			return super().dispatch(request, pk)
    		else:
    			return reverse('not_authorized')
    	except:
    		return redirect(reverse('not_authorized'))


    def get(self, request, *args, **kwargs):
        formset = self.get_formset(turniej=self.kwargs['pk_turniej'])
        return self.render_to_response({'account': self.account,
                                        'formset': formset,
                                        'pk': self.kwargs['pk_turniej'],
                                        'nazwa_turnieju': nazwa_turnieju(self.kwargs['pk_turniej'])})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST, turniej=self.kwargs['pk_turniej'])
        if formset.is_valid():
            formset.save()
            return redirect(reverse("oplata_dynamic_list", kwargs={'pk': self.kwargs['pk_turniej']}))
        return self.render_to_response({'account': self.account,
                                        'formset': formset,
                                        'pk': self.kwargs['pk_turniej'],
                                        'nazwa_turnieju': nazwa_turnieju(self.kwargs['pk_turniej'])})



class UczestnikDeleteView(LoginRequiredMixin, DeleteView):
	login_url = 'start'
	template_name = "wyniki/uczestnik_delete.html"
	context_object_name = 'uczestnik'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk_turniej']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk_turniej'])
		return context

	def get_queryset(self):
		return Wyniki.objects.all()

	def get_success_url(self):
		return reverse("oplata_list", kwargs={'pk': self.kwargs['pk_turniej']})

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.rts:
				return super(UczestnikDeleteView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')




class BronAmunicjaListView(LoginRequiredMixin, ListView):
	login_url = 'start'
	template_name = "wyniki/bron_amunicja_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pk'] = self.kwargs['pk']
		context['nazwa_turnieju'] = nazwa_turnieju(self.kwargs['pk'])
		abr = (Wyniki.objects.filter(zawody__turniej__id = self.kwargs['pk']).values('zawody__nazwa').annotate(acount=Sum('amunicja_klubowa'), bcount=Sum('bron_klubowa')).order_by())
		context['abr'] = abr
		return context

	def get_queryset(self):
		return Wyniki.objects.filter(zawody__turniej__id = self.kwargs['pk']).order_by('zawody')

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.rts or request.user.is_sedzia:
				return super(BronAmunicjaListView, self).dispatch(request, *args, **kwargs)
			else:
				return redirect('not_authorized')
		except:
			return redirect('not_authorized')
			# pass


@login_required(login_url="/start/")
def exportexcelgeneralka(request, pk):
	if request.user.is_admin:
		response=HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename=Wyniki_' + str(datetime.datetime.now())+'.xls'
		wb = xlwt.Workbook(encoding='utf-8')


		grupy_zawodow_w_tym_turnieju = Zawody.objects.filter(turniej__id=pk, zawody_grupa__isnull=False).values_list('zawody_grupa__nazwa', flat=True).order_by('id')

		zawody_grup = {}
		for i in grupy_zawodow_w_tym_turnieju:
			zawody_grup[i] = Zawody.objects.filter(zawody_grupa__nazwa=i).values_list('id', flat=True)

		
		wszystkie_id_zawodow = []
		
		for j in zawody_grup:
			konkurencja_id = []
			for i in zawody_grup[j]:
				konkurencja_id.append(i)
				wszystkie_id_zawodow.append(i)
			zawody_grup[j] = konkurencja_id


		converted_list = [str(element) for element in wszystkie_id_zawodow]
		joined_wszystkie_id_zawodow = ','.join(converted_list)

		rows = []
		for i in zawody_grup:
			converted_list = [str(element) for element in zawody_grup[i]]
			joined_string = ",".join(converted_list)

			wynik_grupowy = Wyniki.objects.raw(f'select wyniki_wyniki.id, account_account.nazwisko, account_account.imie, account_account.klub, sum(wyniki_wyniki.X) as X, sum(wyniki_wyniki.Xx) as dziesiec, sum(wyniki_wyniki.dziewiec) as dziewiec, sum(wyniki_wyniki.osiem) as osiem, sum(wyniki_wyniki.siedem) as siedem, sum(wyniki_wyniki.szesc) as szesc, sum(wyniki_wyniki.piec) as piec, sum(wyniki_wyniki.cztery) as cztery, sum(wyniki_wyniki.trzy) as trzy, sum(wyniki_wyniki.dwa) as dwa, sum(wyniki_wyniki.jeden) as jeden, sum(wyniki_wyniki.X*10 + wyniki_wyniki.Xx*10 + wyniki_wyniki.dziewiec*9 + wyniki_wyniki.osiem*8 + wyniki_wyniki.siedem*7 + wyniki_wyniki.szesc*6 + wyniki_wyniki.piec*5 + wyniki_wyniki.cztery*4 + wyniki_wyniki.trzy*3 + wyniki_wyniki.dwa*2 + wyniki_wyniki.jeden*1) as Wynik from account_account left join wyniki_wyniki on account_account.id = wyniki_wyniki.zawodnik_id left join zawody_zawody on zawody_zawody.id = wyniki_wyniki.zawody_id where zawody_zawody.id in ({joined_string}) group by account_account.id order by Wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC, szesc desc, piec desc, cztery desc, trzy desc, dwa desc, jeden desc')
			rows.append(wynik_grupowy)
			zawody_grup[i] = wynik_grupowy

		wynik_general = Wyniki.objects.raw(f'select wyniki_wyniki.id, account_account.nazwisko, account_account.imie, account_account.klub, sum(wyniki_wyniki.X*10 + wyniki_wyniki.Xx*10 + wyniki_wyniki.dziewiec*9 + wyniki_wyniki.osiem*8 + wyniki_wyniki.siedem*7 + wyniki_wyniki.szesc*6 + wyniki_wyniki.piec*5 + wyniki_wyniki.cztery*4 + wyniki_wyniki.trzy*3 + wyniki_wyniki.dwa*2 + wyniki_wyniki.jeden*1) as Wynik, sum(wyniki_wyniki.dziewiec) as dziewiec, sum(wyniki_wyniki.osiem) as osiem, sum(wyniki_wyniki.siedem) as siedem, sum(wyniki_wyniki.szesc) as szesc, sum(wyniki_wyniki.piec) as piec, sum(wyniki_wyniki.cztery) as cztery, sum(wyniki_wyniki.trzy) as trzy, sum(wyniki_wyniki.dwa) as dwa, sum(wyniki_wyniki.jeden) as jeden from account_account left join wyniki_wyniki on account_account.id = wyniki_wyniki.zawodnik_id left join zawody_zawody on zawody_zawody.id = wyniki_wyniki.zawody_id where zawody_zawody.id in ({joined_wszystkie_id_zawodow}) group by account_account.id order by Wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC, szesc desc, piec desc, cztery desc, trzy desc, dwa desc, jeden desc')
		# print(f'rows: {rows}')


		ws = []
		for i in grupy_zawodow_w_tym_turnieju:
			ws.append(wb.add_sheet(i))

		row_num = 0
		font_style = xlwt.XFStyle()
		font_style.font.bold=True

		columns = ['Pozycja','Nazwisko','Imię', 'Klub', 'Suma']

		for col_num in range(len(columns)):
			for i in ws:
				i.write(row_num, col_num, columns[col_num], font_style)


		font_style = xlwt.XFStyle()
		zawody_id = Zawody.objects.filter(turniej__id=pk).values_list('id', flat=True).order_by('id')
		zawody_id_lista = []
		for i in zawody_id:
			zawody_id_lista.append(i)


		# rows = []
		# for count, i in enumerate(zawody_id_lista):
		# 	rows.append(Wyniki.objects.filter(zawody__id = i, oplata = 1).values_list('zawodnik__nazwisko','zawodnik__imie', 'zawodnik__klub', 'wynik').order_by('-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem', '-szesc', '-piec', '-cztery', '-trzy', '-dwa', '-jeden'))
			# queryset = Wyniki.objects.filter(zawody__id = i, oplata = 1).values_list('zawodnik__nazwisko','zawodnik__imie', 'zawodnik__klub', 'wynik').order_by('-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem', '-szesc', '-piec', '-cztery', '-trzy', '-dwa', '-jeden')
			# items = zip(range(1,queryset.count()+1), queryset)


			# rows.append(items)

		# rows.append(Wyniki.objects.filter(zawody__turniej = pk, oplata = 1).values_list('zawodnik__nazwisko','zawodnik__imie', 'zawodnik__klub', 'X', 'Xx', 'dziewiec', 'osiem', 'siedem', 'szesc', 'piec', 'cztery', 'trzy', 'dwa', 'jeden', 'wynik', 'kara').order_by('-wynik', '-X', '-Xx', '-dziewiec', '-osiem', '-siedem', '-szesc', '-piec', '-cztery', '-trzy', '-dwa', '-jeden'))	
		# generalka = Wyniki.objects.raw('select account_account.nazwisko, account_account.imie, account_account.klub, sum(wynik) as wynik, account_account.id from account_account inner join zawody_zawody on wyniki_wyniki.zawody_id = zawody_zawody.id inner join wyniki_wyniki on account_account.id=wyniki_wyniki.zawodnik_id where zawody_zawody.turniej_id = %s and oplata=1 and wyniki_wyniki.kara = %s group by account_account.id order by wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC', [pk, 'BRAK'])
		# generalka = Wyniki.objects.raw('select wyniki_wyniki.id, zawodnik_id, sum(X) as X, sum(Xx) as Xx,sum(dziewiec) as dziewiec, sum(osiem) as osiem,sum(siedem) as siedem , sum(szesc) as szesc, sum(piec) as piec, sum(cztery) as cztery, sum(trzy) as trzy, sum(dwa) as dwa, sum(jeden) as jeden, sum(wynik) as wynik from wyniki_wyniki inner join zawody_zawody on wyniki_wyniki.zawody_id = zawody_zawody.id where zawody_zawody.turniej_id = %s and oplata=1 and wyniki_wyniki.kara = %s group by zawodnik_id order by wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC', [pk, 'BRAK'])
		# rows.append(generalka)
		# for x,y in enumerate(ws):
		# 	row_num = 0
		# 	for index, row in enumerate(rows[x], start=1):
		# 		row_num +=1
		# 		for col_num in range(len(row)+1):
		# 			if col_num==0:
		# 				y.write(row_num, col_num, index, font_style)
		# 			else:
		# 				y.write(row_num, col_num, str(row[col_num-1]), font_style)

		# print(f'rows[1]: {type(rows[1])}')
		# print(f'wynik_general: {type(wynik_general)}')

		for x,y in enumerate(ws):
			row_num = 0

			for index, row in enumerate(rows[x], start=1):
				# pass

				y.write(index,   0, index, font_style)
				y.write(index, 1, row.nazwisko, font_style)
				y.write(index, 2, row.imie, font_style)
				y.write(index, 3, row.klub, font_style)
				y.write(index, 4, row.Wynik, font_style)




		# klasyfikacja_generalna_display = Turniej.objects.filter(id=pk).values_list('klasyfikacja_generalna', flat=True)
		if 1 == 1:

			ws.append(wb.add_sheet("Klasyfikacja generalna"))
			columns = ['Pozycja','Nazwisko','Imię', 'Klub', 'Suma']
			row_num = 0
			font_style = xlwt.XFStyle()
			font_style.font.bold=True
			for col_num in range(len(columns)):
					ws[len(ws)-1].write(row_num, col_num, columns[col_num], font_style)

			font_style = xlwt.XFStyle()
			tab_generalka = len(ws)-1
			for i,y in enumerate(wynik_general):
				ws[tab_generalka].write(i+1,   0, i+1, font_style)
				ws[tab_generalka].write(i+1, 1, y.nazwisko, font_style)
				ws[tab_generalka].write(i+1, 2, y.imie, font_style)
				ws[tab_generalka].write(i+1, 3, y.klub, font_style)
				ws[tab_generalka].write(i+1, 4, y.Wynik, font_style)


		# ws.append(wb.add_sheet("Sędziowie"))
		# columns = ['Klasa', 'Nazwisko', 'Imię']
		# row_num=0
		# font_style = xlwt.XFStyle()
		# font_style.font.bold=True
		# tab_sedziowie = len(ws)-1

		# for col_num in range(len(columns)):
		# 	ws[tab_sedziowie].write(row_num, col_num, columns[col_num], font_style)



		# font_style = xlwt.XFStyle()
		# sedziowie = Sedzia.objects.filter(zawody__id__in = zawody_id_lista).values_list('sedzia__klasa_sedziego', 'sedzia__nazwisko', 'sedzia__imie').distinct()
		# print(sedziowie)
		# for sedzia in sedziowie:
		# 	row_num +=1
		# 	for col_num in range(len(sedzia)):
		# 		ws[tab_sedziowie].write(row_num, col_num, str(sedzia[col_num]), font_style)




		wb.save(response)

		return(response)

	else:
		return redirect('home')
		
		
		
@login_required(login_url="/start/")
def export_psv_wyniki_general(request, pk):
	context = {}
	context['nazwa_turnieju'] = nazwa_turnieju(pk)
	context['pk'] = pk


	if context['nazwa_turnieju'][0].wyniki_generalne_widoczne and request.user.rts:

		grupy_zawodow_w_tym_turnieju = Zawody.objects.filter(turniej__id=pk, zawody_grupa__isnull=False).values_list('zawody_grupa__nazwa', flat=True)
		# print(f'grupy_zawodow_w_tym_turnieju: {grupy_zawodow_w_tym_turnieju}')
		# for i in grupy_zawodow_w_tym_turnieju:
		# 	print(f'i: {i}')
		zawody_grup = {}
		for i in grupy_zawodow_w_tym_turnieju:
			zawody_grup[i] = Zawody.objects.filter(zawody_grupa__nazwa=i).values_list('id', flat=True)

		zawody_grup_nazwy = zawody_grup


		wszystkie_id_zawodow = []
		
		for j in zawody_grup:
			konkurencja_id = []
			for i in zawody_grup[j]:
				konkurencja_id.append(i)
				wszystkie_id_zawodow.append(i)
			zawody_grup[j] = konkurencja_id


		converted_list = [str(element) for element in wszystkie_id_zawodow]
		joined_wszystkie_id_zawodow = ','.join(converted_list)

		for i in zawody_grup:
			converted_list = [str(element) for element in zawody_grup[i]]
			joined_string = ",".join(converted_list)

			elements = zawody_grup[i]
			# print(f'elements: {elements}')

			select_strings_to_add = []
			display_headings = []
			from_strings_to_add = []

			for num, j in enumerate(elements):
				# print(f'num: {num}')
				select_strings_to_add.append(f'coalesce(w{j}.wynik,"Nie startował") w{num}')
				if context['nazwa_turnieju'][0].turniej_druzynowy:
					display_headings.append(f'{Zawody.objects.filter(id=j).values_list("nazwa", flat=True)[0]}')
				else:
					display_headings.append(f'{Zawody.objects.filter(id=j).values_list("turniej__nazwa", flat=True)[0]}')
				from_strings_to_add.append(f" left join (select wynik, zawodnik_id from wyniki_wyniki where wyniki_wyniki.zawody_id = {j}) w{j} on w{j}.zawodnik_id = account_account.id")

			select_converted = [str(element) for element in select_strings_to_add]
			select_string = ",".join(select_converted)

			from_converted = [str(element) for element in from_strings_to_add]
			from_string = " ".join(from_converted)






			my_string = "sum(wyniki_wyniki.osiem) as osiem, "

			# wynik_grupowy = Wyniki.objects.raw(f'select wyniki_wyniki.id, zawodnik_id from wyniki_wyniki inner join zawody_zawody on wyniki_wyniki.zawody_id = zawody_zawody.id where zawody_zawody.id in ({joined_string})')
			sql_string = "select wyniki_wyniki.id, account_account.nazwisko, account_account.imie,"\
			f"account_account.email, sum(wyniki_wyniki.X) as X, sum(wyniki_wyniki.Xx) as dziesiec, sum(wyniki_wyniki.dziewiec) as dziewiec,"\
			f"sum(wyniki_wyniki.osiem) as osiem, "\
			f"sum(wyniki_wyniki.siedem) as siedem, sum(wyniki_wyniki.szesc) as szesc, sum(wyniki_wyniki.piec) as piec, sum(wyniki_wyniki.cztery) as cztery,"\
			f"sum(wyniki_wyniki.trzy) as trzy, sum(wyniki_wyniki.dwa) as dwa, sum(wyniki_wyniki.jeden) as jeden, " \
			" case count(wyniki_wyniki.wynik) when 4 then sum(wyniki_wyniki.wynik) - min(wyniki_wyniki.wynik) else  sum(wyniki_wyniki.wynik) end Wynik," \
			f" {select_string} "\
			"from account_account "\
			"left join wyniki_wyniki on account_account.id = wyniki_wyniki.zawodnik_id "\
			f"left join zawody_zawody on zawody_zawody.id = wyniki_wyniki.zawody_id "\
			f"{from_string} "\
			f"where zawody_zawody.id in ({joined_string}) "\
			"group by account_account.id "\
			"order by Wynik desc, X desc, Xx desc, dziewiec desc, osiem desc, siedem DESC, szesc desc, piec desc, cztery desc, trzy desc, dwa desc, jeden desc"
			# print(f'sql string : {sql_string}')

			wynik_grupowy = Wyniki.objects.raw(sql_string)
			zawody_grup[i] = {'wynik':wynik_grupowy, 'dupa':display_headings}

		context['wynik_grupowy'] = zawody_grup

		turniej_grup = []

		for i in grupy_zawodow_w_tym_turnieju:
			turniej_grup.append(Zawody.objects.filter(zawody_grupa__nazwa=i).values_list('turniej_id', flat=True))


		turniej_grup_flat = []
		for i in turniej_grup:
			for j in i:
				turniej_grup_flat.append(j)

		turniej_grup_set = sorted(set(turniej_grup_flat))


		for i in turniej_grup_set:
			converted_list = [str(element) for element in turniej_grup_set]
			joined_string_turnieje = ",".join(converted_list)

		select_strings_general = []
		display_headings_general = []
		from_strings_general = []

		for num, j in enumerate(turniej_grup_set):
				# print(f'num: {num}')
			select_strings_general.append(f'coalesce(w{j}.wynik,"Nie startował") w{num}')

			display_headings_general.append(f'{Turniej.objects.filter(id=j).values_list("nazwa", flat=True)[0]}')
			from_strings_general.append(f" left join (select sum(wyniki_wyniki.wynik) wynik, zawodnik_id from wyniki_wyniki join zawody_zawody on wyniki_wyniki.zawody_id = zawody_zawody.id where zawody_zawody.turniej_id={j} group by wyniki_wyniki.zawodnik_id) w{j} on w{j}.zawodnik_id = account_account.id")

		select_converted = [str(element) for element in select_strings_general]
		select_string_general = ",".join(select_converted)

		from_converted = [str(element) for element in from_strings_general]
		from_strings_general = " ".join(from_converted)

################################################

		sql_string = "select account_account.id id, "\
					"account_account.nazwisko, "\
					"account_account.nazwisko||' '||account_account.imie zawodnik, "\
					"account_account.email, "\
					"case count(wall.wynik) when 4 then sum(wall.wynik) - min(wall.wynik) else  sum(wall.wynik) end Wynik, "\
					f"{select_string_general} "\
					"from account_account "\
					f"{from_strings_general} "\
					f"left join (select sum(wyniki_wyniki.wynik) wynik, zawody_turniej.id turniej_id, zawodnik_id from wyniki_wyniki join zawody_zawody on wyniki_wyniki.zawody_id = zawody_zawody.id join zawody_turniej on zawody_turniej.id = zawody_zawody.turniej_id where zawody_turniej.id in ({joined_string_turnieje}) group by wyniki_wyniki.zawodnik_id, zawody_turniej.id) wall on wall.zawodnik_id = account_account.id "\
					"group by account_account.id "\
					"order by Wynik desc "\

		# print(f'sql string: {sql_string}')

		wynik_generalny_sql = Account.objects.raw(sql_string)
		wynik_generalny = {'wynik':wynik_generalny_sql, 'header':display_headings}
		context['wynik_generalny'] = wynik_generalny

#######################################
		content = ''


		for key, value in context['wynik_grupowy'].items():
			content += key+'\n'
			content += 'Lp|Zawodnik|'

			for val in value['dupa']:
				content += f'{val}|'
			content += 'Wynik\n'

			for lp, val in enumerate(value['wynik']):
				# print(f'Val: {vars(val)}')
				if val.Wynik:
					content += f'{lp+1}|{val.nazwisko} {val.imie}|'
					# print(f'val: {val.nazwisko}')
					if 'w0' in vars(val):
						content += str(val.w0) + '|'
						# if val.w0 == 0:
						# 	content += '0|'
					if 'w1' in vars(val):
						content += str(val.w1) + '|'
						# if val.w1 == 0:
						# 	content += '0|'
					if 'w2' in vars(val):
						content += str(val.w2) + '|'
						# if val.w2 == 0:
						# 	content += '0|'
					if 'w3' in vars(val):
						content += str(val.w3) + '|'
						# if val.w3 == 0:
						# 	content += '0|'



					content += str(val.Wynik) + '\n'
				# content += f'{val}\n'


		if not context["nazwa_turnieju"][0].turniej_druzynowy:

		# print(f'cnazwa_turnieju: {context["nazwa_turnieju"][0].turniej_druzynowy}')
			content += 'Podsumowanie \n'
			content += 'Lp|Zawodnik|'
				# for val in context['wynik_generalny']:
			for header in context['wynik_generalny']['header']:
				content += f'{header}|'
			content += 'Wynik\n'
				# for result in context['wynik_generalny']['wynik']:
			for lp, val in enumerate(context['wynik_generalny']['wynik']):
				if val.Wynik:
					content += f'{lp+1}|{val.nazwisko} {val.imie}|'
						# print(f'val: {val.nazwisko}')
					if 'w0' in vars(val):
						content += str(val.w0) + '|'
					if 'w1' in vars(val):
						content += str(val.w1) + '|'
					if 'w2' in vars(val):
						content += str(val.w2) + '|'
					if 'w3' in vars(val):
						content += str(val.w3) + '|'
					content += str(val.Wynik) + '\n'





########################################

		response=HttpResponse(content, content_type='text/plain')
		response['Content-Disposition'] = 'attachment; filename=Wyniki_' + str(datetime.datetime.now())+'.psv'

		
		return(response)



	else:
		return redirect('not_authorized')


