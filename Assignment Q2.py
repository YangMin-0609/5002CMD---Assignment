class UDGraph:
    #Unweighted Directed Graph implementation for social media connections
    #Uses adjacency list representation for efficient edge operations


    def __init__(self):
        # Dictionary to store adjacency lists
        self.adj_list = dict()

    def add_vertex(self, vertex):
        #Add a new vertex to the graph if it doesn't exist
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, from_vertex, to_vertex):
        #Add directed edge from from_vertex to to_vertex
        #Raises ValueError if vertices don't exist

        if from_vertex in self.adj_list and to_vertex in self.adj_list:
            if to_vertex not in self.adj_list[from_vertex]:  # Prevent duplicates
                self.adj_list[from_vertex].append(to_vertex)
        else:
            raise ValueError("One or both vertices not found")

    def remove_edge(self, from_vertex, to_vertex):
        #Remove edge between vertices if it exists
        if from_vertex in self.adj_list:
            if to_vertex in self.adj_list[from_vertex]:
                self.adj_list[from_vertex].remove(to_vertex)
            else:
                raise ValueError("Edge does not exist")
        else:
            raise ValueError("Vertex not found")

    def get_outgoing(self, vertex):
        #Get all outgoing connections (followed accounts)
        return self.adj_list.get(vertex, []).copy()  # Return copy to prevent modification

    def get_incoming(self, vertex):
        #Get all incoming connections (followers)
        followers = []
        for v in self.adj_list:
            if vertex in self.adj_list[v]:
                followers.append(v)
        return followers

    def has_vertex(self, vertex):
        #Check if vertex exists in graph
        return vertex in self.adj_list

    def has_edge(self, from_vertex, to_vertex):
        #Check if directed edge exists
        if from_vertex in self.adj_list:
            return to_vertex in self.adj_list[from_vertex]
        return False

    def get_vertices(self):
        #Get list of all vertices (users)
        return list(self.adj_list.keys())

    def __str__(self):
        #String representation of the graph
        return "\n".join(
            f"{vertex} -> {neighbors}"
            for vertex, neighbors in self.adj_list.items()
        )


class Person:

    def __init__(self, name, gender=None, bio=None, privacy="Public"):
        self.name = name
        self.gender = gender
        self.bio = bio
        self.privacy = privacy  # "Public" or "Private"

    def display_profile(self):
        #Returns formatted profile information based on privacy settings
        profile = f"Name: {self.name}"
        if self.privacy == "Public":
            if self.gender:
                profile += f"\nGender: {self.gender}"
            if self.bio:
                profile += f"\nBio: {self.bio}"
        else:
            profile += "\n[Private Profile - More details hidden]"
        return profile

    def __str__(self):
        return self.name


def initialize_sample_data():
    # Create sample users
    users = {
        "David": Person("david_520", "Female", "Musician | No Music No life ", "Public"),
        "Susanto": Person("SSanto123", "Male", "Digital artist | Cat Cat Cat!", "Public"),
        "Bryan": Person("Bryyann", "Male", "Software engineer | Im a Streamer in Twitch:z7hsfid ", "Private"),
        "Calvin": Person("Ca1Vin", "Male", "Photographer | I love Movie!", "Public"),
        "Miko": Person("ItsMiko", "Female", "Teacher | Master at cooking", "Private")
    }

    # Initialize graph
    social_graph = UDGraph()

    # Add all users to graph
    for name in users:
        social_graph.add_vertex(name)

    # Create follower relationships
    relationships = [
        ("David", "Susanto"), ("David", "Bryan"), ("David", "Miko"),
        ("Miko", "David"), ("Miko", "Calvin"),
        ("Bryan", "David"), ("Bryan", "Susanto"),
        ("Calvin", "Susanto"), ("Susanto", "Bryan")
    ]

    for follower, followed in relationships:
        social_graph.add_edge(follower, followed)

    return users, social_graph


def display_menu():
    #Displays the main menu options#
    print("\n" + "=" * 40)
    print("SlowGram - Social Media App")
    print("=" * 40)
    print("1. View all user profiles")
    print("2. View detailed profile")
    print("3. View accounts followed by user")
    print("4. View user's followers")
    print("5. Add new user profile")
    print("6. Follow another user")
    print("7. Unfollow a user")
    print("8. Exit")
    print("=" * 40)


def main():
    """Main program loop"""
    users, graph = initialize_sample_data()

    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ")

        if choice == "1":  # View all users
            print("\nAll Users:")
            for i, name in enumerate(users.keys(), 1):
                print(f"{i}. {name}")

        elif choice == "2":  # View detailed profile
            name = input("Enter username: ")
            if name in users:
                print("\n" + users[name].display_profile())
            else:
                print("User not found!")

        elif choice == "3":  # View followed accounts
            name = input("Enter username: ")
            if graph.has_vertex(name):
                following = graph.get_outgoing(name)
                if following:
                    print(f"\n{name} follows:")
                    for user in following:
                        print(f"- {user}")
                else:
                    print(f"\n{name} isn't following anyone")
            else:
                print("User not found!")

        elif choice == "4":  # View followers
            name = input("Enter username: ")
            if graph.has_vertex(name):
                followers = graph.get_incoming(name)
                if followers:
                    print(f"\n{name} is followed by:")
                    for user in followers:
                        print(f"- {user}")
                else:
                    print(f"\n{name} has no followers")
            else:
                print("User not found!")

        elif choice == "5":  # Add new user
            name = input("Enter new username: ")
            if name not in users:
                privacy = input("Privacy (Public/Private): ").capitalize()
                bio = input("Bio (optional): ")
                users[name] = Person(name, bio=bio, privacy=privacy)
                graph.add_vertex(name)
                print(f"User {name} created successfully!")
            else:
                print("Username already exists!")

        elif choice == "6":  # Follow user
            follower = input("Your username: ")
            to_follow = input("Username to follow: ")
            if graph.has_vertex(follower) and graph.has_vertex(to_follow):
                if not graph.has_edge(follower, to_follow):
                    graph.add_edge(follower, to_follow)
                    print(f"{follower} is now following {to_follow}!")
                else:
                    print(f"{follower} already follows {to_follow}")
            else:
                print("One or both usernames not found!")

        elif choice == "7":  # Unfollow user
            follower = input("Your username: ")
            to_unfollow = input("Username to unfollow: ")
            if graph.has_vertex(follower) and graph.has_vertex(to_unfollow):
                if graph.has_edge(follower, to_unfollow):
                    graph.remove_edge(follower, to_unfollow)
                    print(f"{follower} unfollowed {to_unfollow}!")
                else:
                    print(f"{follower} doesn't follow {to_unfollow}")
            else:
                print("One or both usernames not found!")

        elif choice == "8":  # Exit
            print("Thanks for using SlowGram. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()