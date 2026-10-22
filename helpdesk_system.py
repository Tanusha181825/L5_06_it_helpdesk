"""IT helpdesk ticket management system."""
import os
import socket
import json
from datetime import datetime


# Global state
tickets = {}
ADMIN_PASSWORD = os.environ.get("HELPDESK_ADMIN_PASSWORD")


def raise_ticket(user, issue_type, urgency="3", audit_trail=None):
    """Create a helpdesk ticket and record its creation."""
    if audit_trail is None:
        audit_trail = []
    try:
        urgency = int(urgency)
    except (ValueError, TypeError) as exc:
        raise ValueError("Urgency must be an integer from 1 to 5") from exc

    if not 1 <= urgency <= 5:
        raise ValueError("Urgency must be between 1 and 5")
    ticket_id = max(tickets.keys(), default=100) + 1
    tickets[ticket_id] = {
        "user": user,
        "issue": issue_type,
        "priority": urgency,
        "tech": None,
        "notes": []
    }
    audit_trail.append(
        f"{user} raised #{ticket_id} at {datetime.now()}"
    )
    return ticket_id


def assign_ticket(ticket_id, technician):
    """Assign a technician to a ticket."""
    tickets[ticket_id]["tech"] = technician


def add_note(ticket_id, note):
    """Add a note to an existing ticket."""
    if ticket_id in tickets:
        tickets[ticket_id]["notes"].append(note)
    else:
        print(f"Ticket #{ticket_id} not found.")


def close_ticket(ticket_id, password):
    """Close a ticket after verifying the admin password."""
    if password == ADMIN_PASSWORD:
        del tickets[ticket_id]


def unresolved_high_priority():
    """Return IDs of unassigned high-priority tickets."""
    result = []
    for ticket_id, ticket in tickets.items():
        if ticket["priority"] >= 4 and ticket["tech"] is None:
            result.append(ticket_id)
    return result


def ping_user_machine(hostname):
    """Check whether a hostname resolves to an IP address."""
    try:
        socket.gethostbyname(hostname)
        return 0
    except socket.gaierror:
        return 1


def save_tickets(file="tickets.json"):
    """Save all tickets to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(tickets, output_file)


def main():
    """Demonstrate helpdesk ticket operations."""
    t1 = raise_ticket("anil", "printer", "5")
    raise_ticket("meera", "wifi", "4")
    t3 = raise_ticket("joe", "vpn", "3")
    assign_ticket(t1, "Tech-Kiran")
    add_note(999, "Called user")
    print("Unassigned high priority:", unresolved_high_priority())
    level = (
        input("Urgency for a new laptop ticket (1-5, Enter for 3): ")
        or "3"
    )
    raise_ticket("sana", "laptop", level)
    if ADMIN_PASSWORD:
        close_ticket(t3, ADMIN_PASSWORD)
    save_tickets()
    print("Open tickets:", list(tickets.keys()))


main()
