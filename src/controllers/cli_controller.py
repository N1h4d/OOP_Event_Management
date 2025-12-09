# src/controllers/cli_controller.py
from ..utils.validators import (
    normalize_name,
    normalize_full_name,
    validate_positive_int,
    validate_price,
    validate_phone,
    validate_email,
    validate_gender,
    validate_date,
    validate_time,
    validate_yes_no,
)


from ..logging_config import get_logger

from ..repositories.venue_repository import VenueRepository
from ..repositories.event_repository import EventRepository
from ..repositories.participant_repository import ParticipantRepository
from ..repositories.ticket_repository import TicketRepository

from ..services.venue_service import VenueService
from ..services.event_service import EventService
from ..services.participant_service import ParticipantService
from ..services.ticket_service import TicketService

logger = get_logger(__name__)


class CLIController:
    """
    GRASP Controller:
    - Handles all user interactions (input/output)
    - Delegates business logic to Services
    - Services use Repositories to access the database
    """

    def __init__(self, connection):
        # Repositories
        venue_repo = VenueRepository(connection)
        event_repo = EventRepository(connection)
        participant_repo = ParticipantRepository(connection)
        ticket_repo = TicketRepository(connection)

        # Services
        self._venue_service = VenueService(venue_repo)
        self._event_service = EventService(event_repo)
        self._participant_service = ParticipantService(participant_repo)
        self._ticket_service = TicketService(ticket_repo)

    # ===================== MAIN LOOP ===================== #

    def run(self):
        """
        Main CLI loop.
        """
        logger.info("CLIController started.")
        while True:
            print("\n=== Event Management System ===")
            print("1.  Create Venue")
            print("2.  List Venues")
            print("3.  Update Venue")
            print("4.  Delete Venue")
            print("5.  Create Event")
            print("6.  List Events")
            print("7.  Update Event")
            print("8.  Delete Event")
            print("9.  Create Participant")
            print("10. List Participants")
            print("11. Update Participant")
            print("12. Delete Participant")
            print("13. Sell Ticket")
            print("14. List Tickets")
            print("15. Update Ticket")
            print("16. Delete Ticket")
            print("0.  Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.create_venue()
            elif choice == "2":
                self.list_venues()
            elif choice == "3":
                self.update_venue()
            elif choice == "4":
                self.delete_venue()
            elif choice == "5":
                self.create_event()
            elif choice == "6":
                self.list_events()
            elif choice == "7":
                self.update_event()
            elif choice == "8":
                self.delete_event()
            elif choice == "9":
                self.create_participant()
            elif choice == "10":
                self.list_participants()
            elif choice == "11":
                self.update_participant()
            elif choice == "12":
                self.delete_participant()
            elif choice == "13":
                self.sell_ticket()
            elif choice == "14":
                self.list_tickets()
            elif choice == "15":
                self.update_ticket()
            elif choice == "16":
                self.delete_ticket()
            elif choice == "0":
                print("Exiting...")
                logger.info("User exited the application from CLIController.")
                break
            else:
                print("Invalid choice. Please try again.")

    # ===================== VENUE ===================== #

    def create_venue(self):
        print("\n--- Create Venue ---")
        try:
            # Name
            while True:
                try:
                    raw_name = input("Venue name: ")
                    name = normalize_name(raw_name)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            # Address (boş ola bilməz)
            while True:
                address = input("Address: ").strip()
                if address:
                    break
                print("Error: Address is required.")

            # Capacity
            while True:
                try:
                    raw_capacity = input("Capacity: ")
                    capacity = validate_positive_int(raw_capacity, "Capacity")
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            # Manager name
            while True:
                try:
                    raw_manager = input("Manager name: ")
                    manager_name = normalize_full_name(raw_manager)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            # Phone
            while True:
                try:
                    raw_phone = input("Phone (e.g. 0501234567): ")
                    phone = validate_phone(raw_phone)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            venue = self._venue_service.create_venue(
                name=name,
                address=address,
                capacity=capacity,
                manager_name=manager_name,
                phone=phone,
                is_open=True
            )

            print("\nVenue successfully created:")
            print(venue.display_info())

        except Exception as ex:
            print(f"Unexpected error while creating venue: {ex}")
            logger.error("Error while creating venue: %s", ex)

    def list_venues(self):
        print("\n--- List of Venues ---")
        venues = self._venue_service.list_venues()
        if not venues:
            print("No venues found.")
            return

        for v in venues:
            print("-" * 40)
            print(v.display_info())

    def update_venue(self):
        try:
            print("\n--- Update Venue ---")
            venues = self._venue_service.list_venues()
            if not venues:
                print("No venues found.")
                return

            for idx, v in enumerate(venues, start=1):
                print(f"{idx}. {v.name} (ID={v.id})")

            choice_str = input("Choose venue to update (number): ").strip()
            if not choice_str.isdigit():
                raise ValueError("Invalid selection.")
            index = int(choice_str) - 1
            if index < 0 or index >= len(venues):
                raise ValueError("Index out of range.")

            selected = venues[index]

            print("\nLeave field empty to keep current value.")

            name = input(f"Name [{selected.name}]: ").strip() or selected.name
            address = input(f"Address [{selected.address}]: ").strip() or selected.address

            capacity_str = input(f"Capacity [{selected.capacity}]: ").strip()
            capacity = selected.capacity if capacity_str == "" else int(capacity_str)

            manager_name = (
                input(f"Manager [{selected.manager_name}]: ").strip()
                or selected.manager_name
            )
            phone = input(f"Phone [{selected.phone}]: ").strip() or selected.phone

            is_open_str = input(
                f"Is open? (y/n) [current={'y' if selected.is_open else 'n'}]: "
            ).strip().lower()
            if is_open_str == "":
                is_open = selected.is_open
            else:
                is_open = is_open_str == "y"

            updated = self._venue_service.update_venue(
                venue_id=selected.id,
                name=name,
                address=address,
                capacity=capacity,
                manager_name=manager_name,
                phone=phone,
                is_open=is_open
            )

            print("\nVenue successfully updated:")
            print(updated.display_info())

        except ValueError as ex:
            print(f"Error: {ex}")
            logger.error("Error while updating venue: %s", ex)

    def delete_venue(self):
        try:
            print("\n--- Delete Venue ---")
            venues = self._venue_service.list_venues()
            if not venues:
                print("No venues found.")
                return

            for idx, v in enumerate(venues, start=1):
                print(f"{idx}. {v.name} (ID={v.id})")

            choice_str = input("Choose venue to delete (number): ").strip()
            if not choice_str.isdigit():
                raise ValueError("Invalid selection.")
            index = int(choice_str) - 1
            if index < 0 or index >= len(venues):
                raise ValueError("Index out of range.")

            selected = venues[index]

            confirm = input(
                f"Are you sure you want to delete '{selected.name}'? (y/n): "
            ).strip().lower()
            if confirm != "y":
                print("Delete cancelled.")
                return

            self._venue_service.delete_venue(selected.id)
            print("Venue deleted successfully.")

        except ValueError as ex:
            print(f"Error: {ex}")
            logger.error("Error while deleting venue: %s", ex)

    # ===================== EVENT ===================== #

    def create_event(self):
        print("\n--- Create Event ---")
        try:
            name = input("Event name: ").strip()
            if not name:
                print("Error: Event name is required.")
                return

            category = input("Category: ").strip()
            description = input("Description: ").strip()

            # Date
            while True:
                try:
                    raw_date = input("Date (YYYY-MM-DD): ")
                    date = validate_date(raw_date)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            # Time
            while True:
                try:
                    raw_time = input("Time (HH:MM): ")
                    time = validate_time(raw_time)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            # Duration
            while True:
                try:
                    raw_duration = input("Duration (minutes): ")
                    duration = validate_positive_int(raw_duration, "Duration")
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            # mövcud venue-ları göstər
            venues = self._venue_service.list_venues()
            if not venues:
                print("No venues found. Please create a venue first.")
                return

            print("\nAvailable venues:")
            for idx, v in enumerate(venues, start=1):
                print(f"{idx}. {v.name} (ID={v.id})")

            while True:
                venue_choice_str = input("Choose venue (number): ").strip()
                if not venue_choice_str.isdigit():
                    print("Error: Invalid venue selection.")
                    continue
                venue_index = int(venue_choice_str) - 1
                if venue_index < 0 or venue_index >= len(venues):
                    print("Error: Venue index out of range.")
                    continue
                selected_venue = venues[venue_index]
                break

            event = self._event_service.create_event(
                name=name,
                date=date,
                time=time,
                category=category,
                description=description,
                duration_minutes=duration,
                venue_id=selected_venue.id,
                is_active=True
            )

            print("\nEvent successfully created:")
            print(event.display_info())

        except Exception as ex:
            print(f"Unexpected error while creating event: {ex}")
            logger.error("Error while creating event: %s", ex)


    def list_events(self):
        print("\n--- List of Events ---")
        events = self._event_service.list_events()
        if not events:
            print("No events found.")
            return

        for e in events:
            print("-" * 40)
            print(e.display_info())

    def update_event(self):
        try:
            print("\n--- Update Event ---")
            events = self._event_service.list_events()
            if not events:
                print("No events found.")
                return

            for idx, e in enumerate(events, start=1):
                print(f"{idx}. {e.name} on {e.date} (ID={e.id})")

            while True:
                choice_str = input("Choose event to update (number): ").strip()
                if not choice_str.isdigit():
                    print("❌ Invalid selection.")
                    continue
                index = int(choice_str) - 1
                if 0 <= index < len(events):
                    selected = events[index]
                    break
                else:
                    print("❌ Index out of range.")

            print("\nPress Enter to keep current value.\n")

            # NAME
            raw = input(f"Name [{selected.name}]: ").strip()
            name = raw if raw else selected.name

            # DATE
            while True:
                raw = input(f"Date [{selected.date}]: ").strip()
                if raw == "":
                    date = selected.date
                    break
                try:
                    date = validate_date(raw)
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            # TIME
            while True:
                raw = input(f"Time [{selected.time}]: ").strip()
                if raw == "":
                    time = selected.time
                    break
                try:
                    time = validate_time(raw)
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            # CATEGORY
            raw = input(f"Category [{selected.category}]: ").strip()
            category = raw if raw else selected.category

            # DESCRIPTION
            raw = input(f"Description [{selected.description}]: ").strip()
            description = raw if raw else selected.description

            # DURATION
            while True:
                raw = input(f"Duration [{selected.duration_minutes}]: ").strip()
                if raw == "":
                    duration = selected.duration_minutes
                    break
                try:
                    duration = validate_positive_int(raw, "Duration")
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            # VENUE
            venues = self._venue_service.list_venues()
            print("\nAvailable venues:")
            for idx, v in enumerate(venues, start=1):
                print(f"{idx}. {v.name}")

            while True:
                raw = input("Choose venue (Enter = keep current): ").strip()
                if raw == "":
                    venue_id = selected.venue_id
                    break
                if not raw.isdigit():
                    print("❌ Invalid venue selection.")
                    continue
                venue_index = int(raw) - 1
                if 0 <= venue_index < len(venues):
                    venue_id = venues[venue_index].id
                    break
                else:
                    print("❌ Venue index out of range.")

            # IS ACTIVE
            while True:
                raw = input(
                    f"Is active? (y/n) [current={'y' if selected.is_active else 'n'}]: "
                ).strip()
                if raw == "":
                    is_active = selected.is_active
                    break
                try:
                    is_active = validate_yes_no(raw, "Is active")
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            updated = self._event_service.update_event(
                event_id=selected.id,
                name=name,
                date=date,
                time=time,
                category=category,
                description=description,
                duration_minutes=duration,
                venue_id=venue_id,
                is_active=is_active
            )

            print("\n✅ Event successfully updated:")
            print(updated.display_info())

        except Exception as ex:
            print(f"Unexpected error: {ex}")
            logger.error("Error while updating event: %s", ex)


    def delete_event(self):
        try:
            print("\n--- Delete Event ---")
            events = self._event_service.list_events()
            if not events:
                print("No events found.")
                return

            for idx, e in enumerate(events, start=1):
                print(f"{idx}. {e.name} on {e.date} (ID={e.id})")

            choice_str = input("Choose event to delete (number): ").strip()
            if not choice_str.isdigit():
                raise ValueError("Invalid selection.")
            index = int(choice_str) - 1
            if index < 0 or index >= len(events):
                raise ValueError("Index out of range.")

            selected = events[index]

            confirm = input(
                f"Are you sure you want to delete '{selected.name}'? (y/n): "
            ).strip().lower()
            if confirm != "y":
                print("Delete cancelled.")
                return

            self._event_service.delete_event(selected.id)
            print("Event deleted successfully.")

        except ValueError as ex:
            print(f"Error: {ex}")
            logger.error("Error while deleting event: %s", ex)

    # ===================== PARTICIPANT ===================== #

    def create_participant(self):
        print("\n--- Create Participant ---")
        try:
            # Full name
            while True:
                try:
                    raw_name = input("Full name: ")
                    full_name = normalize_full_name(raw_name)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            # Email
            while True:
                try:
                    raw_email = input("Email: ")
                    email = validate_email(raw_email)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            # Phone
            while True:
                try:
                    raw_phone = input("Phone (e.g. 0501234567): ")
                    phone = validate_phone(raw_phone)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            # Age
            while True:
                try:
                    raw_age = input("Age: ")
                    age = validate_positive_int(raw_age, "Age")
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            # Gender
            while True:
                try:
                    raw_gender = input("Gender (M/F): ")
                    gender = validate_gender(raw_gender)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            # Registration date
            while True:
                try:
                    raw_date = input("Registration date (YYYY-MM-DD): ")
                    registration_date = validate_date(raw_date)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            # Is VIP
            while True:
                try:
                    raw_vip = input("Is VIP? (y/n): ")
                    is_vip = validate_yes_no(raw_vip, "Is VIP")
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            participant = self._participant_service.create_participant(
                full_name=full_name,
                email=email,
                phone=phone,
                age=age,
                gender=gender,
                registration_date=registration_date,
                is_vip=is_vip
            )

            print("\nParticipant successfully created:")
            print(participant.display_info())

        except Exception as ex:
            print(f"Unexpected error while creating participant: {ex}")
            logger.error("Error while creating participant: %s", ex)


    def list_participants(self):
        print("\n--- List of Participants ---")
        participants = self._participant_service.list_participants()
        if not participants:
            print("No participants found.")
            return

        for p in participants:
            print("-" * 40)
            print(p.display_info())


    def update_participant(self):
        try:
            print("\n--- Update Participant ---")
            participants = self._participant_service.list_participants()
            if not participants:
                print("No participants found.")
                return

            for idx, p in enumerate(participants, start=1):
                print(f"{idx}. {p.full_name} (ID={p.id})")

            while True:
                choice_str = input("Choose participant to update (number): ").strip()
                if not choice_str.isdigit():
                    print("❌ Invalid selection.")
                    continue
                index = int(choice_str) - 1
                if 0 <= index < len(participants):
                    selected = participants[index]
                    break
                else:
                    print("❌ Index out of range.")

            print("\nPress Enter to keep current value.\n")

            # FULL NAME
            while True:
                raw = input(f"Full name [{selected.full_name}]: ").strip()
                if raw == "":
                    full_name = selected.full_name
                    break
                try:
                    full_name = normalize_full_name(raw)
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            # EMAIL
            while True:
                raw = input(f"Email [{selected.email}]: ").strip()
                if raw == "":
                    email = selected.email
                    break
                try:
                    email = validate_email(raw)
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            # PHONE
            while True:
                raw = input(f"Phone [{selected.phone}]: ").strip()
                if raw == "":
                    phone = selected.phone
                    break
                try:
                    phone = validate_phone(raw)
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            # AGE
            while True:
                raw = input(f"Age [{selected.age}]: ").strip()
                if raw == "":
                    age = selected.age
                    break
                try:
                    age = validate_positive_int(raw, "Age")
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            # GENDER
            while True:
                raw = input(f"Gender [{selected.gender}]: ").strip()
                if raw == "":
                    gender = selected.gender
                    break
                try:
                    gender = validate_gender(raw)
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            # REGISTRATION DATE
            while True:
                raw = input(f"Registration date [{selected.registration_date}]: ").strip()
                if raw == "":
                    registration_date = selected.registration_date
                    break
                try:
                    registration_date = validate_date(raw)
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            # IS VIP
            while True:
                raw = input(
                    f"Is VIP? (y/n) [current={'y' if selected.is_vip else 'n'}]: "
                ).strip()
                if raw == "":
                    is_vip = selected.is_vip
                    break
                try:
                    is_vip = validate_yes_no(raw, "Is VIP")
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            updated = self._participant_service.update_participant(
                participant_id=selected.id,
                full_name=full_name,
                email=email,
                phone=phone,
                age=age,
                gender=gender,
                registration_date=registration_date,
                is_vip=is_vip
            )

            print("\n✅ Participant successfully updated:")
            print(updated.display_info())

        except Exception as ex:
            print(f"Unexpected error: {ex}")
            logger.error("Error while updating participant: %s", ex)


    def delete_participant(self):
        try:
            print("\n--- Delete Participant ---")
            participants = self._participant_service.list_participants()
            if not participants:
                print("No participants found.")
                return

            for idx, p in enumerate(participants, start=1):
                print(f"{idx}. {p.full_name} (ID={p.id})")

            choice_str = input("Choose participant to delete (number): ").strip()
            if not choice_str.isdigit():
                raise ValueError("Invalid selection.")
            index = int(choice_str) - 1
            if index < 0 or index >= len(participants):
                raise ValueError("Index out of range.")

            selected = participants[index]

            confirm = input(
                f"Are you sure you want to delete '{selected.full_name}'? (y/n): "
            ).strip().lower()
            if confirm != "y":
                print("Delete cancelled.")
                return

            self._participant_service.delete_participant(selected.id)
            print("Participant deleted successfully.")

        except ValueError as ex:
            print(f"Error: {ex}")
            logger.error("Error while deleting participant: %s", ex)

    # ===================== TICKET ===================== #

    def sell_ticket(self):
        print("\n--- Sell Ticket ---")
        try:
            # 1) Event seç
            events = self._event_service.list_events()
            if not events:
                print("No events found. Please create an event first.")
                return

            print("\nAvailable events:")
            for idx, e in enumerate(events, start=1):
                print(f"{idx}. {e.name} on {e.date} (ID={e.id})")

            while True:
                event_choice_str = input("Choose event (number): ").strip()
                if not event_choice_str.isdigit():
                    print("Error: Invalid event selection.")
                    continue
                event_index = int(event_choice_str) - 1
                if event_index < 0 or event_index >= len(events):
                    print("Error: Event index out of range.")
                    continue
                selected_event = events[event_index]
                break

            # 2) Participant seç
            participants = self._participant_service.list_participants()
            if not participants:
                print("No participants found. Please create a participant first.")
                return

            print("\nAvailable participants:")
            for idx, p in enumerate(participants, start=1):
                print(f"{idx}. {p.full_name} (ID={p.id})")

            while True:
                participant_choice_str = input("Choose participant (number): ").strip()
                if not participant_choice_str.isdigit():
                    print("Error: Invalid participant selection.")
                    continue
                participant_index = int(participant_choice_str) - 1
                if participant_index < 0 or participant_index >= len(participants):
                    print("Error: Participant index out of range.")
                    continue
                selected_participant = participants[participant_index]
                break

            # 3) Ticket məlumatları
            while True:
                try:
                    raw_price = input("Base price: ")
                    price = validate_price(raw_price)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            while True:
                seat_number = input("Seat number: ").strip()
                if seat_number:
                    break
                print("Error: Seat number is required.")

            while True:
                ticket_type = input("Ticket type (Standard/VIP/Student): ").strip()
                if ticket_type:
                    break
                print("Error: Ticket type is required.")

            while True:
                try:
                    raw_date = input("Purchase date (YYYY-MM-DD): ")
                    purchase_date = validate_date(raw_date)
                    break
                except ValueError as e:
                    print(f"Error: {e}")

            ticket = self._ticket_service.sell_ticket(
                event_id=selected_event.id,
                participant_id=selected_participant.id,
                price=price,
                seat_number=seat_number,
                ticket_type=ticket_type,
                purchase_date=purchase_date,
                is_used=False
            )

            print("\nTicket successfully sold:")
            print(ticket.display_info())

        except Exception as ex:
            print(f"Unexpected error while selling ticket: {ex}")
            logger.error("Error while selling ticket: %s", ex)


    def list_tickets(self):
        print("\n--- List of Tickets ---")
        tickets = self._ticket_service.list_tickets()
        if not tickets:
            print("No tickets found.")
            return

        for t in tickets:
            print("-" * 40)
            print(t.display_info())

    def update_ticket(self):
        try:
            print("\n--- Update Ticket ---")
            tickets = self._ticket_service.list_tickets()
            if not tickets:
                print("No tickets found.")
                return

            for idx, t in enumerate(tickets, start=1):
                print(
                    f"{idx}. Ticket ID={t.id} | Event={t.event_id} | Participant={t.participant_id}"
                )

            while True:
                choice_str = input("Choose ticket to update (number): ").strip()
                if not choice_str.isdigit():
                    print("❌ Invalid selection.")
                    continue
                index = int(choice_str) - 1
                if 0 <= index < len(tickets):
                    selected = tickets[index]
                    break
                else:
                    print("❌ Index out of range.")

            print("\nPress Enter to keep current value.\n")

            # PRICE
            while True:
                raw = input(f"Price [{selected.price}]: ").strip()
                if raw == "":
                    price = selected.price
                    break
                try:
                    price = validate_price(raw)
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            # SEAT NUMBER
            raw = input(f"Seat number [{selected.seat_number}]: ").strip()
            seat_number = raw if raw else selected.seat_number

            # TICKET TYPE
            raw = input(f"Ticket type [{selected.ticket_type}]: ").strip()
            ticket_type = raw if raw else selected.ticket_type

            # PURCHASE DATE
            while True:
                raw = input(f"Purchase date [{selected.purchase_date}]: ").strip()
                if raw == "":
                    purchase_date = selected.purchase_date
                    break
                try:
                    purchase_date = validate_date(raw)
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            # IS USED
            while True:
                raw = input(
                    f"Is used? (y/n) [current={'y' if selected.is_used else 'n'}]: "
                ).strip()
                if raw == "":
                    is_used = selected.is_used
                    break
                try:
                    is_used = validate_yes_no(raw, "Is used")
                    break
                except ValueError as e:
                    print(f"❌ {e}")

            updated = self._ticket_service.update_ticket(
                ticket_id=selected.id,
                event_id=selected.event_id,
                participant_id=selected.participant_id,
                price=price,
                seat_number=seat_number,
                ticket_type=ticket_type,
                purchase_date=purchase_date,
                is_used=is_used
            )

            print("\n✅ Ticket successfully updated:")
            print(updated.display_info())

        except Exception as ex:
            print(f"Unexpected error: {ex}")
            logger.error("Error while updating ticket: %s", ex)


    def delete_ticket(self):
        try:
            print("\n--- Delete Ticket ---")
            tickets = self._ticket_service.list_tickets()
            if not tickets:
                print("No tickets found.")
                return

            for idx, t in enumerate(tickets, start=1):
                print(f"{idx}. Ticket ID={t.id} | Event={t.event_id} | Participant={t.participant_id}")

            choice_str = input("Choose ticket to delete (number): ").strip()
            if not choice_str.isdigit():
                raise ValueError("Invalid selection.")
            index = int(choice_str) - 1
            if index < 0 or index >= len(tickets):
                raise ValueError("Index out of range.")

            selected = tickets[index]

            confirm = input(
                f"Are you sure you want to delete ticket '{selected.id}'? (y/n): "
            ).strip().lower()
            if confirm != "y":
                print("Delete cancelled.")
                return

            self._ticket_service.delete_ticket(selected.id)
            print("Ticket deleted successfully.")

        except ValueError as ex:
            print(f"Error: {ex}")
            logger.error("Error while deleting ticket: %s", ex)
