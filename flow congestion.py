import tkinter as tk
import time
import threading
import random

#____________________________________________________________________________________________

                                #DEVELOPED BY RAHUL BHARWDAJ

#____________________________________________________________________________________________

class FlowControlGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flow and Congestion Control")
        self.root.geometry("1400x700")

        self.canvas = tk.Canvas(root, width=1300, height=600, bg='white')
        self.canvas.pack()

        title_label = tk.Label(root, text="Flow and Congestion Control", font=("Arial", 24, "bold"))
        title_label.pack()

        self.protocol = tk.StringVar(value='Stop-and-Wait')
        selection_frame = tk.Frame(root)
        selection_frame.pack()

        tk.Label(selection_frame, text="Select Protocol:", font=("Arial", 18)).pack(side=tk.LEFT)
        tk.Radiobutton(selection_frame, text="Stop-and-Wait", variable=self.protocol, value='Stop-and-Wait', font=("Arial", 16)).pack(side=tk.LEFT)
        tk.Radiobutton(selection_frame, text="Sliding Window", variable=self.protocol, value='Sliding Window', font=("Arial", 16)).pack(side=tk.LEFT)

        self.start_button = tk.Button(root, text="Start Simulation", font=("Arial", 18, "bold"), bg="lightblue", command=self.start_simulation)
        self.start_button.pack(pady=10)

        self.canvas.create_rectangle(50, 250, 200, 400, fill='gray')
        self.canvas.create_rectangle(1100, 250, 1250, 400, fill='gray')
        self.canvas.create_text(125, 420, text="Sender (Computer A)", font=("Arial", 18, "bold"))
        self.canvas.create_text(1175, 420, text="Receiver (Computer B)", font=("Arial", 18, "bold"))

        self.label_developer = tk.Label(root, text="Developed by Rahul", font=("Arial", 16, "bold"), fg="blue")
        self.label_developer.pack()
#____________________________________________________________________________________________
    def start_simulation(self):
        self.canvas.delete("packet")
        self.canvas.delete("ack")
        self.canvas.delete("timeout_text")
        if self.protocol.get() == 'Stop-and-Wait':
            threading.Thread(target=self.stop_and_wait).start()
        else:
            threading.Thread(target=self.sliding_window).start()
#____________________________________________________________________________________________
    def stop_and_wait(self):
        packet_number = 1
        while packet_number <= 5:
            packet_x = 220
            packet_y = 310
            packet = self.canvas.create_rectangle(packet_x, packet_y, packet_x + 50, packet_y + 30, fill='blue', tags="packet")
            packet_text = self.canvas.create_text(packet_x + 25, packet_y + 15, text=f"P{packet_number}", font=("Arial", 12), fill='white', tags="packet_text")
            self.move_packet(packet, packet_text, 220, 1100)

            # Simulate ACK
            time.sleep(random.uniform(0.5, 1.5)) # Simulate varying network delay
            ack_received = random.choice([True, False]) # Simulate ACK success or failure

            if ack_received:
                ack_text = self.canvas.create_text(1175, 200, text=f"ACK {packet_number}", fill='green', font=("Arial", 18, "bold"), tags="ack")
                time.sleep(0.8)
                self.canvas.delete("ack")
                self.canvas.delete("packet")
                self.canvas.delete("packet_text")
                time.sleep(0.3)
                packet_number += 1
            else:
                # Simulate ACK loss - Sender times out and resends
                timeout_text = self.canvas.create_text(125, 220, text=f"Timeout, Resending P{packet_number}", fill='red', font=("Arial", 16, "bold"), tags="timeout_text")
                time.sleep(1.2)
                self.canvas.delete("timeout_text")
                self.canvas.delete("packet")
                self.canvas.delete("packet_text")
                time.sleep(0.2)

#_____________________________________________________________________________________________
    def sliding_window(self):
        window_size = 3
        total_packets = 6
        base = 1
        next_packet_number = 1

        while base <= total_packets:
            window_end = min(base + window_size - 1, total_packets)

            for i in range(next_packet_number, window_end + 1):
                packet_x = 220 + (i - base) * 60
                packet_y = 310
                packet = self.canvas.create_rectangle(packet_x, packet_y, packet_x + 50, packet_y + 30, fill='blue', tags=f"packet_{i}")
                packet_text = self.canvas.create_text(packet_x + 25, packet_y + 15, text=f"P{i}", font=("Arial", 12), fill='white', tags=f"packet_text_{i}")
                self.move_packet(packet, packet_text, 220 + (i - base) * 60, 1100, packet_id=i)
                time.sleep(0.2)

            next_packet_number = window_end + 1

            # Simulate ACKs
            ack_received_up_to = 0
            for i in range(base, window_end + 1):
                if random.random() > 0.3: # Simulate a chance of successful ACK
                    ack_received_up_to = i
                else:
                    print(f"Simulating no ACK for Packet {i} and onwards")
                    break # Stop simulating ACKs after a potential loss

            if ack_received_up_to >= base:
                ack_text = self.canvas.create_text(1175, 200, text=f"ACK {ack_received_up_to}", fill='green', font=("Arial", 18, "bold"), tags="ack")
                time.sleep(1)
                self.canvas.delete("ack")

                for i in range(base, ack_received_up_to + 1):
                    if f"packet_{i}" in self.canvas.gettags("all"):
                        self.canvas.delete(f"packet_{i}")
                        self.canvas.delete(f"packet_text_{i}")
                base = ack_received_up_to + 1
            else:
                # Simulate no ACK received for the current window - timeout will eventually trigger resend
                timeout_text = self.canvas.create_text(125, 220, text=f"No ACK received for packets {base}-{window_end} (Simulated)", fill='orange', font=("Arial", 16, "bold"), tags="timeout_text")
                time.sleep(1.5)
                self.canvas.delete("timeout_text")
                # In a real system, a timer would expire, and packets would be retransmitted.
                # For simplicity, the next iteration of the loop will try to resend.

            time.sleep(0.5)
#__________________________________________________________________________________________
    def move_packet(self, packet, packet_text, start_x, end_x, packet_id=None):
        for x in range(start_x, end_x, 10):
            self.canvas.move(packet, 10, 0)
            self.canvas.move(packet_text, 10, 0)
            self.root.update()
            time.sleep(0.03)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlowControlGUI(root)
    root.mainloop()