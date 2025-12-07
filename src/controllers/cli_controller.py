# src/controllers/cli_controller.py

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
        try:
            print("\n--- Create Venue ---")
            name = input("Venue name: ").strip()
            address = input("Address: ").strip()
            capacity_str = input("Capacity: ").strip()
            manager_name = input("Manager name: ").strip()
            phone = input("Phone: ").strip()

            if not capacity_str.isdigit():
                raise ValueError("Capacity must be a positive integer.")

            capacity = int(capacity_str)

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

        except ValueError as ex:
            print(f"Error: {ex}")
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
        try:
            print("\n--- Create Event ---")
            name = input("Event name: ").strip()
            date = input("Date (YYYY-MM-DD): ").strip()
            time = input("Time (HH:MM): ").strip()
            category = input("Category: ").strip()
            description = input("Description: ").strip()
            duration_str = input("Duration (minutes): ").strip()

            if not duration_str.isdigit():
                raise ValueError("Duration must be a positive integer.")
            duration = int(duration_str)

            # mövcud venue-ları göstər
            venues = self._venue_service.list_venues()
            if not venues:
                print("No venues found. Please create a venue first.")
                return

            print("\nAvailable venues:")
            for idx, v in enumerate(venues, start=1):
                print(f"{idx}. {v.name} (ID={v.id})")

            venue_choice_str = input("Choose venue (number): ").strip()
            if not venue_choice_str.isdigit():
                raise ValueError("Invalid venue selection.")

            venue_index = int(venue_choice_str) - 1
            if venue_index < 0 or venue_index >= len(venues):
                raise ValueError("Venue index out of range.")

            selected_venue = venues[venue_index]

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

        except ValueError as ex:
            print(f"Error: {ex}")
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

            choice_str = input("Choose event to update (number): ").strip()
            if not choice_str.isdigit():
                raise ValueError("Invalid selection.")
            index = int(choice_str) - 1
            if index < 0 or index >= len(events):
                raise ValueError("Index out of range.")

            selected = events[index]

            print("\nLeave field empty to keep current value.")

            name = input(f"Name [{selected.name}]: ").strip() or selected.name
            date = input(f"Date [{selected.date}]: ").strip() or selected.date
            time = input(f"Time [{selected.time}]: ").strip() or selected.time
            category = input(f"Category [{selected.category}]: ").strip() or selected.category
            description = (
                input(f"Description [{selected.description}]: ").strip()
                or selected.description
            )

            duration_str = input(
                f"Duration (minutes) [{selected.duration_minutes}]: "
            ).strip()
            duration = (
                selected.duration_minutes
                if duration_str == ""
                else int(duration_str)
            )

            # Venue dəyişmək istəyirsə
            venues = self._venue_service.list_venues()
            if not venues:
                print("No venues found. Please create a venue first.")
                return

            print("\nAvailable venues:")
            for idx, v in enumerate(venues, start=1):
                print(f"{idx}. {v.name} (ID={v.id})")
            print("Press Enter to keep current venue.")

            venue_choice_str = input("Choose venue (number): ").strip()
            if venue_choice_str == "":
                venue_id = selected.venue_id
            else:
                if not venue_choice_str.isdigit():
                    raise ValueError("Invalid venue selection.")
                venue_index = int(venue_choice_str) - 1
                if venue_index < 0 or venue_index >= len(venues):
                    raise ValueError("Venue index out of range.")
                venue_id = venues[venue_index].id

            is_active_str = input(
                f"Is active? (y/n) [current={'y' if selected.is_active else 'n'}]: "
            ).strip().lower()
            if is_active_str == "":
                is_active = selected.is_active
            else:
                is_active = is_active_str == "y"

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

            print("\nEvent successfully updated:")
            print(updated.display_info())

        except ValueError as ex:
            print(f"Error: {ex}")
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
        try:
            print("\n--- Create Participant ---")
            full_name = input("Full name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            age_str = input("Age: ").strip()
            gender = input("Gender (M/F): ").strip()
            registration_date = input("Registration date (YYYY-MM-DD): ").strip()
            is_vip_str = input("Is VIP? (y/n): ").strip().lower()

            if not age_str.isdigit():
                raise ValueError("Age must be a positive integer.")
            age = int(age_str)

            is_vip = is_vip_str == "y"

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

        except ValueError as ex:
            print(f"Error: {ex}")
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

            choice_str = input("Choose participant to update (number): ").strip()
            if not choice_str.isdigit():
                raise ValueError("Invalid selection.")
            index = int(choice_str) - 1
            if index < 0 or index >= len(participants):
                raise ValueError("Index out of range.")

            selected = participants[index]

            print("\nLeave field empty to keep current value.")

            full_name = (
                input(f"Full name [{selected.full_name}]: ").strip()
                or selected.full_name
            )
            email = input(f"Email [{selected.email}]: ").strip() or selected.email
            phone = input(f"Phone [{selected.phone}]: ").strip() or selected.phone

            age_str = input(f"Age [{selected.age}]: ").strip()
            age = selected.age if age_str == "" else int(age_str)

            gender = (
                input(f"Gender [{selected.gender}]: ").strip()
                or selected.gender
            )
            registration_date = (
                input(f"Registration date [{selected.registration_date}]: ").strip()
                or selected.registration_date
            )

            is_vip_str = input(
                f"Is VIP? (y/n) [current={'y' if selected.is_vip else 'n'}]: "
            ).strip().lower()
            if is_vip_str == "":
                is_vip = selected.is_vip
            else:
                is_vip = is_vip_str == "y"

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

            print("\nParticipant successfully updated:")
            print(updated.display_info())

        except ValueError as ex:
            print(f"Error: {ex}")
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
        try:
            print("\n--- Sell Ticket ---")

            # 1) Event seç
            events = self._event_service.list_events()
            if not events:
                print("No events found. Please create an event first.")
                return

            print("\nAvailable events:")
            for idx, e in enumerate(events, start=1):
                print(f"{idx}. {e.name} on {e.date} (ID={e.id})")

            event_choice_str = input("Choose event (number): ").strip()
            if not event_choice_str.isdigit():
                raise ValueError("Invalid event selection.")
            event_index = int(event_choice_str) - 1
            if event_index < 0 or event_index >= len(events):
                raise ValueError("Event index out of range.")
            selected_event = events[event_index]

            # 2) Participant seç
            participants = self._participant_service.list_participants()
            if not participants:
                print("No participants found. Please create a participant first.")
                return

            print("\nAvailable participants:")
            for idx, p in enumerate(participants, start=1):
                print(f"{idx}. {p.full_name} (ID={p.id})")

            participant_choice_str = input("Choose participant (number): ").strip()
            if not participant_choice_str.isdigit():
                raise ValueError("Invalid participant selection.")
            participant_index = int(participant_choice_str) - 1
            if participant_index < 0 or participant_index >= len(participants):
                raise ValueError("Participant index out of range.")
            selected_participant = participants[participant_index]

            # 3) Ticket məlumatları
            price_str = input("Base price: ").strip()
            if not price_str.replace(".", "", 1).isdigit():
                raise ValueError("Price must be a non-negative number.")
            price = float(price_str)

            seat_number = input("Seat number: ").strip()
            ticket_type = input("Ticket type (Standard/VIP/Student): ").strip()
            purchase_date = input("Purchase date (YYYY-MM-DD): ").strip()

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

        except ValueError as ex:
            print(f"Error: {ex}")
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
                print(f"{idx}. Ticket ID={t.id} | Event={t.event_id} | Participant={t.participant_id}")

            choice_str = input("Choose ticket to update (number): ").strip()
            if not choice_str.isdigit():
                raise ValueError("Invalid selection.")
            index = int(choice_str) - 1
            if index < 0 or index >= len(tickets):
                raise ValueError("Index out of range.")

            selected = tickets[index]

            print("\nLeave field empty to keep current value.")

            price_str = input(f"Price [{selected.price}]: ").strip()
            if price_str == "":
                price = selected.price
            else:
                if not price_str.replace(".", "", 1).isdigit():
                    raise ValueError("Price must be a non-negative number.")
                price = float(price_str)

            seat_number = (
                input(f"Seat number [{selected.seat_number}]: ").strip()
                or selected.seat_number
            )
            ticket_type = (
                input(f"Ticket type [{selected.ticket_type}]: ").strip()
                or selected.ticket_type
            )
            purchase_date = (
                input(f"Purchase date [{selected.purchase_date}]: ").strip()
                or selected.purchase_date
            )

            is_used_str = input(
                f"Is used? (y/n) [current={'y' if selected.is_used else 'n'}]: "
            ).strip().lower()
            if is_used_str == "":
                is_used = selected.is_used
            else:
                is_used = is_used_str == "y"

            # event_id və participant_id-ni dəyişmirik (istəsən sonra genişləndirə bilərik)
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

            print("\nTicket successfully updated:")
            print(updated.display_info())

        except ValueError as ex:
            print(f"Error: {ex}")
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
