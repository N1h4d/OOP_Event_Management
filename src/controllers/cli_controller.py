from ..repositories.venue_repository import VenueRepository
from ..repositories.event_repository import EventRepository
from ..repositories.participant_repository import ParticipantRepository
from ..repositories.ticket_repository import TicketRepository

from ..models.venue import Venue
from ..models.event import Event
from ..models.participant import Participant
from ..models.ticket import Ticket


class CLIController:
    """
    GRASP Controller – istifadəçi ilə interaksiyanı idarə edən təbəqə.
    """

    def __init__(self, connection):
        self._venue_repo = VenueRepository(connection)
        self._event_repo = EventRepository(connection)
        self._participant_repo = ParticipantRepository(connection)
        self._ticket_repo = TicketRepository(connection)

    def run(self):
        while True:
            print("\n=== Event Management System ===")
            print("1. Create Venue")
            print("2. List Venues")
            print("3. Create Event")
            print("4. List Events")
            print("5. Create Participant")
            print("6. List Participants")
            print("7. Sell Ticket")
            print("8. List Tickets")
            print("0. Exit")

            choice = input("Select option: ")

            if choice == "1":
                self.create_venue()
            elif choice == "2":
                self.list_venues()
            elif choice == "3":
                self.create_event()
            elif choice == "4":
                self.list_events()
            elif choice == "5":
                self.create_participant()
            elif choice == "6":
                self.list_participants()
            elif choice == "7":
                self.sell_ticket()
            elif choice == "8":
                self.list_tickets()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

    # ----- Venue -----

    def create_venue(self):
        print("\n-- Create Venue --")
        name = input("Venue name: ")
        address = input("Address: ")
        capacity = int(input("Capacity: "))
        manager_name = input("Manager name: ")
        phone = input("Phone: ")

        venue = Venue(
            name=name,
            address=address,
            capacity=capacity,
            manager_name=manager_name,
            phone=phone
        )
        self._venue_repo.add(venue)
        print("Created:", venue.display_info())

    def list_venues(self):
        print("\n-- Venues --")
        venues = self._venue_repo.get_all()
        if not venues:
            print("No venues found.")
            return
        for v in venues:
            print(" -", v.display_info())

    # ----- Event -----

    def create_event(self):
        print("\n-- Create Event --")
        name = input("Event name: ")
        date = input("Date (YYYY-MM-DD): ")
        time = input("Time (HH:MM): ")
        category = input("Category (e.g. Concert, Conference): ")
        description = input("Description: ")
        duration = int(input("Duration (minutes): "))

        venues = self._venue_repo.get_all()
        if not venues:
            print("No venues available. Create a venue first.")
            return

        print("Available venues:")
        for idx, v in enumerate(venues, start=1):
            print(f"{idx}. {v.display_info()}")

        try:
            index = int(input("Select venue number: "))
            venue = venues[index - 1]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return

        event = Event(
            name=name,
            date=date,
            time=time,
            category=category,
            description=description,
            duration_minutes=duration,
            venue_id=venue.id
        )
        self._event_repo.add(event)
        print("Created:", event.display_info())

    def list_events(self):
        print("\n-- Events --")
        events = self._event_repo.get_all()
        if not events:
            print("No events found.")
            return
        for e in events:
            print(" -", e.display_info())

    # ----- Participant -----

    def create_participant(self):
        print("\n-- Create Participant --")
        full_name = input("Full name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        age = int(input("Age: "))
        gender = input("Gender (M/F/Other): ")
        registration_date = input("Registration date (YYYY-MM-DD): ")
        vip_input = input("Is VIP? (y/n): ").lower()
        is_vip = vip_input == "y"

        participant = Participant(
            full_name=full_name,
            email=email,
            phone=phone,
            age=age,
            gender=gender,
            registration_date=registration_date,
            is_vip=is_vip
        )
        self._participant_repo.add(participant)
        print("Created:", participant.display_info())

    def list_participants(self):
        print("\n-- Participants --")
        participants = self._participant_repo.get_all()
        if not participants:
            print("No participants found.")
            return
        for p in participants:
            print(" -", p.display_info())

    # ----- Ticket -----

    def sell_ticket(self):
        print("\n-- Sell Ticket --")

        events = self._event_repo.get_all()
        if not events:
            print("No events available.")
            return

        print("Available events:")
        for idx, e in enumerate(events, start=1):
            print(f"{idx}. {e.display_info()}")

        try:
            e_idx = int(input("Select event: "))
            event = events[e_idx - 1]
        except (ValueError, IndexError):
            print("Invalid event selection.")
            return

        participants = self._participant_repo.get_all()
        if not participants:
            print("No participants available.")
            return

        print("Participants:")
        for idx, p in enumerate(participants, start=1):
            print(f"{idx}. {p.display_info()}")

        try:
            p_idx = int(input("Select participant: "))
            participant = participants[p_idx - 1]
        except (ValueError, IndexError):
            print("Invalid participant selection.")
            return

        price = float(input("Ticket price: "))
        seat_number = input("Seat number: ")
        ticket_type = input("Ticket type (Regular/VIP/etc.): ")
        purchase_date = input("Purchase date (YYYY-MM-DD): ")

        ticket = Ticket(
            event_id=event.id,
            participant_id=participant.id,
            price=price,
            seat_number=seat_number,
            ticket_type=ticket_type,
            purchase_date=purchase_date
        )
        self._ticket_repo.add(ticket)
        print("Created:", ticket.display_info())

    def list_tickets(self):
        print("\n-- Tickets --")
        tickets = self._ticket_repo.get_all()
        if not tickets:
            print("No tickets found.")
            return
        for t in tickets:
            print(" -", t.display_info())
