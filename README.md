# VisitorApp
When a visitor checkin on this WebApp to meet a host,host will immediatel get the details of the visitor.
When the visitor checks out he will get mail regarding his visit.

## Demo link:(https://visitorpp01.herokuapp.com/)

## Tools Used:
* Django
* Ajax
* Html
* Twilio(for messaging)
* Smtp(for mailing)

### Running the server:
1. Clone the repository
2. Install the 'requirements.txt' file `pip install -r requirements.txt`
3. Make Migrations `python manage.py makemigrations`
4. Migrate the database `python manage.py migrate`
5. Create a SuperUser `python manage.py createsuperuser`
6. Run the server `python manage.py runserver`

By visiting the admin page(localhost/admin) host details can be added which is used by visitor during checkin.
