#!/usr/bin/env python3
"""
Load Testing Script for Odoo 19 Production
Tests concurrent users, response times, and system stability
"""
import requests
import time
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import sys

class OdooLoadTester:
    def __init__(self, base_url="http://localhost:8069", num_users=10, duration=60):
        self.base_url = base_url
        self.num_users = num_users
        self.duration = duration
        self.session = requests.Session()
        self.response_times = []
        self.errors = 0
        self.requests_made = 0

    def login(self):
        """Simple connectivity check - just verify we can access Odoo"""
        try:
            response = self.session.get(f"{self.base_url}/web", timeout=10)
            if response.status_code == 200:
                print(f"✅ Connected to Odoo at {self.base_url}")
                return True
            else:
                print(f"❌ Failed to connect: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def make_request(self, endpoint="/web", params=None):
        """Make a simple web request to Odoo"""
        start_time = time.time()

        try:
            # Make a simple GET request to test basic connectivity
            response = self.session.get(
                f"{self.base_url}{endpoint}",
                timeout=30
            )

            response_time = time.time() - start_time
            self.response_times.append(response_time)
            self.requests_made += 1

            if response.status_code == 200:
                return True, response_time
            else:
                self.errors += 1
                return False, response_time

        except Exception as e:
            response_time = time.time() - start_time
            self.response_times.append(response_time)
            self.errors += 1
            return False, response_time

    def user_simulation(self, user_id):
        """Simulate a single user"""
        print(f"🚀 Starting user {user_id}")

        if not self.login():
            print(f"❌ User {user_id} failed to connect")
            return

        end_time = time.time() + self.duration

        while time.time() < end_time:
            # Simulate different types of simple web requests
            endpoints = [
                "/web",
                "/web/login",
                "/odoo",
                "/web/webclient/load_menus",
                "/web/webclient/translations?lang=en_US"
            ]

            for endpoint in endpoints:
                success, response_time = self.make_request(endpoint)
                if not success:
                    print(f"⚠️  User {user_id} request failed ({response_time:.3f}s)")
                else:
                    print(f"✅ User {user_id} request success ({response_time:.3f}s)")

                # Random delay between requests (0.5-2 seconds)
                time.sleep(0.5 + (time.time() % 1.5))

        print(f"🏁 User {user_id} completed")

    def run_load_test(self):
        """Run the load test"""
        print("🚀 STARTING ODOO LOAD TEST")
        print(f"   Target: {self.base_url}")
        print(f"   Users: {self.num_users}")
        print(f"   Duration: {self.duration}s")
        print("=" * 50)

        start_time = time.time()

        # Create thread pool for concurrent users
        with ThreadPoolExecutor(max_workers=self.num_users) as executor:
            futures = [
                executor.submit(self.user_simulation, i)
                for i in range(self.num_users)
            ]

            # Wait for all users to complete
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Thread error: {e}")

        total_time = time.time() - start_time

        # Calculate statistics
        self.print_results(total_time)

    def print_results(self, total_time):
        """Print test results"""
        print("\n" + "=" * 50)
        print("📊 LOAD TEST RESULTS")
        print("=" * 50)

        if self.response_times:
            print(f"⏱️  Total test time: {total_time:.2f}s")
            print(f"👥 Total users: {self.num_users}")
            print(f"📨 Total requests: {self.requests_made}")
            print(f"❌ Total errors: {self.errors}")
            print(f"📈 Requests/second: {self.requests_made/total_time:.2f}")
            print(f"📉 Error rate: {(self.errors/self.requests_made)*100:.2f}%" if self.requests_made > 0 else "0%")

            print("\n⏱️  Response Time Statistics:")
            print(f"   Average: {statistics.mean(self.response_times):.3f}s")
            print(f"   Median: {statistics.median(self.response_times):.3f}s")
            print(f"   Min: {min(self.response_times):.3f}s")
            print(f"   Max: {max(self.response_times):.3f}s")
            print(f"   95th percentile: {statistics.quantiles(self.response_times, n=20)[18]:.3f}s")

            # Performance rating
            avg_response = statistics.mean(self.response_times)
            if avg_response < 1.0:
                rating = "🟢 EXCELLENT"
            elif avg_response < 3.0:
                rating = "🟡 GOOD"
            elif avg_response < 5.0:
                rating = "🟠 FAIR"
            else:
                rating = "🔴 POOR"

            print(f"\n🎯 Performance Rating: {rating}")

            # Recommendations
            print("\n💡 Recommendations:")
            if avg_response > 5.0:
                print("   - Consider increasing server resources")
                print("   - Optimize database queries")
                print("   - Implement caching")
            elif avg_response > 3.0:
                print("   - Monitor resource usage")
                print("   - Consider load balancer for high traffic")
            else:
                print("   - System performing well")
                print("   - Ready for production")

        else:
            print("❌ No requests completed - check system connectivity")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Odoo Load Testing Tool')
    parser.add_argument('--url', default='http://localhost:8069',
                       help='Odoo base URL (default: http://localhost:8069)')
    parser.add_argument('--users', type=int, default=5,
                       help='Number of concurrent users (default: 5)')
    parser.add_argument('--duration', type=int, default=30,
                       help='Test duration in seconds (default: 30)')

    args = parser.parse_args()

    tester = OdooLoadTester(args.url, args.users, args.duration)
    tester.run_load_test()

if __name__ == "__main__":
    main()