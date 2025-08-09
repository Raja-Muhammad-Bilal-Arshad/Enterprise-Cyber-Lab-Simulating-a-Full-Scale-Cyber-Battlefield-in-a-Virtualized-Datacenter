#!/usr/bin/env python3
import threading
import time
from scapy.all import IP, ICMP, send

# Simple ICMP packet sender worker
def send_icmp(dst_ip, count):
    pkt = IP(dst=dst_ip) / ICMP()
    for _ in range(count):
        send(pkt, verbose=False)

def test_performance(dst_ip, threads, packets_per_thread):
    thread_list = []
    start = time.time()

    for _ in range(threads):
        t = threading.Thread(target=send_icmp, args=(dst_ip, packets_per_thread))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    end = time.time()
    duration = end - start
    total_packets = threads * packets_per_thread
    pps = total_packets / duration if duration > 0 else 0
    return duration, total_packets, pps

def main():
    print("=== PC Network Sending Capacity Test ===")
    dst_ip = input("Enter a safe target IP (e.g., 127.0.0.1 or gateway IP): ").strip()
    print("Starting test. The script will increase load stepwise.")
    max_threads = 200  # upper cap, adjust if needed
    max_packets = 1000  # packets per thread max cap

    best_threads = 0
    best_packets = 0
    best_pps = 0

    # Step sizes to increase load smoothly
    thread_step = 10
    packet_step = 100

    # We will try increasing threads first, then packets
    for threads in range(thread_step, max_threads + 1, thread_step):
        for packets in range(packet_step, max_packets + 1, packet_step):
            print(f"Testing {threads} threads x {packets} packets each...")
            try:
                duration, total_packets, pps = test_performance(dst_ip, threads, packets)
            except Exception as e:
                print(f"Error during sending: {e}")
                print("Stopping test due to error.")
                return

            print(f"  -> Sent {total_packets} packets in {duration:.2f} seconds, PPS: {pps:.0f}")

            # Update best if performance improves
            if pps > best_pps:
                best_threads = threads
                best_packets = packets
                best_pps = pps
            else:
                # Performance not improving or degrading, stop testing higher packets
                break

        # Optional: Stop increasing threads if performance worsens too much
        if threads > thread_step and pps < best_pps * 0.7:
            print("Performance dropped significantly; stopping thread increase.")
            break

    print("\n=== Test Summary ===")
    print(f"Best performance: {best_threads} threads with {best_packets} packets each")
    print(f"Max throughput: {best_pps:.0f} packets per second")

if __name__ == "__main__":
    main()
