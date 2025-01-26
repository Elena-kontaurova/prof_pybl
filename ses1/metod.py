''' jhjh'''
from datetime import date, datetime
from table_mysql import Guest, Applications, Employees, Visits, Passes


class MetodGuest:
    ''' класс для методов пользователей'''
    @staticmethod
    def get_all_guest():
        ''' получение всех пользователей'''
        guest = Guest.select()
        return [{'id': guests.id, 'first_name': guests.first_name,
                 'last_name': guests.last_name, 'email': guests.email,
                 'phone': guests.phone}
                for guests in guest]

    @staticmethod
    def get_all_guest_number(guest_id: int):
        ''' получение по id'''
        guest = Guest.get(Guest.id == guest_id)
        return {'id': guest.id, 'first_name': guest.first_name,
                'last_name': guest.last_name, 'email': guest.email,
                'phone': guest.phone}

    @staticmethod
    def greate_guest(first_name: str, last_name: str,
                     email: str, phone: str):
        ''' создание нового пользователя'''
        guest = Guest.create(first_name=first_name, last_name=last_name,
                             email=email, phone=phone)
        return {
            'first_name': guest.first_name,
            'last_name': guest.last_name,
            'email': guest.email,
            'phone': guest.phone
        }

    @staticmethod
    def update_guest(gue_id: int, first_name: str, last_name: str,
                     email: str, phone: str):
        ''' обновление пользователя'''
        guest = Guest.get(Guest.id == gue_id)
        guest.first_name = first_name
        guest.last_name = last_name
        guest.email = email
        guest.phone = phone
        guest.save()
        return {
            'id': guest.id,
            'first_name': guest.first_name,
            'last_name': guest.last_name,
            'email': guest.email,
            'phone': guest.phone
        }

    @staticmethod
    def delete_guest(guest_id: int):
        ''' удаление пользователя'''
        guest = Guest.get(Guest.id == guest_id)
        guest.delete_instance()


class MetodApplication:
    ''' класс методов applications'''
    @staticmethod
    def get_all_application():
        ''' получение всех заявок'''
        aplic = Applications.select()
        return [{'id': aplica.id, 'guest': aplica.guest,
                 'application_date': aplica.apllication_date,
                 'status': aplica.status, 'visit_data': aplica.visit_date}
                for aplica in aplic]

    @staticmethod
    def get_number_application(applic_id: int):
        ''' получение заявки по id'''
        applic = Applications.get(Applications.id == applic_id)
        return {'id': applic.id, 'guest': applic.guest,
                'application_date': applic.apllication_date,
                'status': applic.status, 'visit_data': applic.visit_date}

    @staticmethod
    def create_application(guest: int, apllication_date: date,
                           status: str, visit_date: date):
        ''' создание заявки'''
        aplic = Applications.create(guest=guest, apllication_date=apllication_date,
                                    status=status, visit_date=visit_date)
        return {
            'guest': aplic.guest,
            'aplication_date': aplic.apllication_date,
            'status': aplic.status,
            'visit_date': aplic.visit_date
        }

    @staticmethod
    def upddate_application(aplic_id: int, guest: int, apllication_date: date,
                            status: str, visit_date: date):
        ''' обновление записи'''
        aplic = Applications.get(Applications.id == aplic_id)
        aplic.guest = guest
        aplic.apllication_date = apllication_date
        aplic.status = status
        aplic.visit_date = visit_date
        aplic.save()
        return {
            'guest': aplic.guest,
            'apllication_date': aplic.apllication_date,
            'status': aplic.status,
            'visit_date': aplic.visit_date
        }

    @staticmethod
    def delete_application(aplic_id: int):
        ''' удаление записи'''
        alic = Applications.get(Applications.id == aplic_id)
        alic.delete_instance()


class MetodEmployees:
    ''' класс методов Employees'''
    @staticmethod
    def get_all_employ():
        ''' просмотр всех сотрудников'''
        employ = Employees.select()
        return [{'id': emplo.id, 'first_name': emplo.first_name,
                 'last_name': emplo.last_name, 'departament': emplo.departament}
                for emplo in employ]

    @staticmethod
    def get_num_employ(employ_id: str):
        ''' просмотр сотрудника по id'''
        employ = Employees.get(Employees.id == employ_id)
        return {'id': employ.id, 'first_name': employ.first_name,
                'last_name': employ.last_name, 'departament': employ.departament}

    @staticmethod
    def create_employ(first_name: str, last_name: str, departament: str):
        ''' создание сотрудника'''
        emplo = Employees.create(first_name=first_name, last_name=last_name,
                                 departament=departament)
        return {
            'first_name': emplo.first_name,
            'last_name': emplo.last_name,
            'departament': emplo.departament
        }

    @staticmethod
    def update_emply(eploy_id: int, first_name: str, last_name: str,
                     departament: str):
        ''' обновление сотрудника'''
        eploy = Employees.get(Employees.id == eploy_id)
        eploy.first_name = first_name
        eploy.last_name = last_name
        eploy.departament = departament
        eploy.save()
        return {
            'first_name': eploy.first_name,
            'last_name': eploy.last_name,
            'departament': eploy.departament
        }

    @staticmethod
    def delete_employ(eploy_id: int):
        ''' удаление сотрудника по id'''
        emplo = Employees.get(Employees.id == eploy_id)
        emplo.delete_instance()


class MetodVisits:
    ''' класс поcещений'''
    @staticmethod
    def get_all_visit():
        ''' получение всех визитов'''
        visit = Visits.select()
        return [{'id': visi.id, 'application': visi.application,
                 'visit_time': visi.visit_time, 'check_in': visi.check_in,
                 'chech_out': visi.chech_out}
                for visi in visit]

    @staticmethod
    def get_num_visit(visit_id: int):
        ''' получение видита по id'''
        visit = Visits.get(Visits.id == visit_id)
        return {'id': visit.id, 'application': visit.application,
                'visit_time': visit.visit_time, 'check_in': visit.check_in,
                'chech_out': visit.chech_out}

    @staticmethod
    def create_visit(application: int, visit_time: datetime,
                     check_in: datetime, chech_out: datetime):
        ''' создание визита'''
        visit = Visits.create(application=application, visit_time=visit_time,
                              check_in=check_in, chech_out=chech_out)
        return {
            'application': visit.application,
            'visit_time': visit.visit_time,
            'check_in': visit.check_in,
            'chech_out': visit.chech_out
        }

    @staticmethod
    def update_visit(visit_id: int, application: int, visit_time: datetime,
                     check_in: datetime, chech_out: datetime):
        ''' обновление информации о визите'''
        visit = Visits.get(Visits.id == visit_id)
        visit.application = application
        visit.visit_time = visit_time
        visit.check_in = check_in
        visit.chech_out = chech_out
        visit.save()
        return {
            'id': visit.id,
            'application': visit.application,
            'visit_time': visit.visit_time,
            'check_in': visit.check_in,
            'chech_put': visit.chech_out
        }

    @staticmethod
    def delete_visit(visit_id: int):
        ''' удаление записи о визите'''
        visit = Visits.get(Visits.id == visit_id)
        visit.delete_instance()


class MetodPasses:
    ''' класс Passes'''
    @staticmethod
    def get_all_passes():
        ''' получение всех пропусков'''
        pas = Passes.select()
        return [{'id': passes.id, 'applications': passes.applications,
                 'issue_date': passes.issue_date, 'expiry_data': passes.expiry_data,
                 'status': passes.status}
                for passes in pas]

    @staticmethod
    def get_num_passes(pas_id):
        ''' получение пропуска по id'''
        pas = Passes.get(Passes.id == pas_id)
        return {'id': pas.id, 'applications': pas.applications,
                'issue_date': pas.issue_date, 'expiry_data': pas.expiry_data,
                'status': pas.status}

    @staticmethod
    def create_passes(applications: int, issue_date: date,
                      expiry_data: date, status: str):
        ''' создание нового пропуска'''
        pas = Passes.create(applications=applications, issue_date=issue_date,
                            expiry_data=expiry_data, status=status)
        return {
            'applications': pas.applications,
            'issue_date': pas.issue_date,
            'expiry_data': pas.expiry_data,
            'status': pas.status
        }

    @staticmethod
    def update_passes(pas_id: int, applications: int, issue_date: date,
                      expiry_data: date, status: str):
        ''' обновление пропуска'''
        pas = Passes.get(Passes.id == pas_id)
        pas.applications = applications
        pas.issue_date = issue_date
        pas.expiry_data = expiry_data
        pas.status = status
        pas.save()
        return {
            'id': pas.id,
            'applications': pas.applications,
            'issue_date': pas.issue_date,
            'expiry_data': pas.expiry_data,
            'status': pas.status
        }

    @staticmethod
    def delete_passes(pas_id: int):
        ''' удаление записи о пропуске'''
        pas = Passes.get(Passes.id == pas_id)
        pas.delete_instance()
