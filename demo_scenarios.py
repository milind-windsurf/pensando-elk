#!/usr/bin/env python3
"""
Demo Scenarios for NIC Firmware Mock System
Demonstrates various failure scenarios and recovery procedures
"""

import time
import json
import subprocess
import sys
from nic_firmware_mock import MockNICFirmwareSystem, FirmwareStatus, HealthStatus

class DemoScenarios:
    def __init__(self):
        self.system = MockNICFirmwareSystem()
        self.system.initialize_cards(3)  # Initialize 3 cards for demo
        
    def print_banner(self, title):
        print("\n" + "="*60)
        print(f"  {title}")
        print("="*60)
        
    def print_step(self, step, description):
        print(f"\n[STEP {step}] {description}")
        print("-" * 50)
        
    def wait_for_user(self, message="Press Enter to continue..."):
        input(f"\n{message}")
        
    def show_card_status(self, card_id=None):
        """Display current status of cards"""
        if card_id:
            status = self.system.get_card_status(card_id)
            print(json.dumps(status, indent=2))
        else:
            status = self.system.list_cards()
            for cid, card_info in status.items():
                print(f"\n{cid}: Status={card_info['status']}, Health={card_info['health']}")
                
    def scenario_1_normal_installation(self):
        """Scenario 1: Normal firmware installation"""
        self.print_banner("SCENARIO 1: Normal Firmware Installation")
        
        self.print_step(1, "Initial card status")
        self.show_card_status("nic-00")
        self.wait_for_user()
        
        self.print_step(2, "Installing firmware on nic-00")
        success = self.system.install_firmware("nic-00")
        
        self.print_step(3, "Post-installation status")
        self.show_card_status("nic-00")
        
        if success:
            print("\n✅ Installation completed successfully!")
        else:
            print("\n❌ Installation failed!")
            
        self.wait_for_user()
        
    def scenario_2_installation_failure(self):
        """Scenario 2: Installation failure with recovery"""
        self.print_banner("SCENARIO 2: Installation Failure & Recovery")
        
        card = self.system.cards["nic-01"]
        
        self.print_step(1, "Simulating installation failure")
        card.status = FirmwareStatus.FAILED
        card.health = HealthStatus.CRITICAL
        card.error_count = 25
        
        self.show_card_status("nic-01")
        self.wait_for_user()
        
        self.print_step(2, "Detecting anomalies")
        anomalies = self.system.detect_anomalies("nic-01")
        print("Anomalies detected:")
        for anomaly in anomalies:
            print(f"  - {anomaly}")
        self.wait_for_user()
        
        self.print_step(3, "Generating technical support bundle")
        tech_file = self.system.generate_tech_support("nic-01")
        print(f"Tech support bundle: {tech_file}")
        self.wait_for_user()
        
        self.print_step(4, "Executing recovery procedure")
        success = self.system.recovery_procedure("nic-01")
        
        self.print_step(5, "Post-recovery status")
        self.show_card_status("nic-01")
        
        if success:
            print("\n✅ Recovery completed successfully!")
        else:
            print("\n❌ Recovery failed!")
            
        self.wait_for_user()
        
    def scenario_3_health_monitoring(self):
        """Scenario 3: Continuous health monitoring with alerts"""
        self.print_banner("SCENARIO 3: Health Monitoring & Alerts")
        
        self.print_step(1, "Starting health monitoring")
        
        cards_to_monitor = ["nic-00", "nic-01", "nic-02"]
        
        for i in range(5):  # 5 monitoring cycles
            print(f"\n--- Monitoring Cycle {i+1} ---")
            
            for card_id in cards_to_monitor:
                health_data = self.system.check_card_health(card_id)
                print(f"{card_id}: Health={health_data['health_status']}, "
                      f"Temp={health_data['temperature']:.1f}°C, "
                      f"Errors={health_data['error_count']}")
                
                anomalies = self.system.detect_anomalies(card_id)
                if anomalies:
                    print(f"  ⚠️  Anomalies: {', '.join(anomalies)}")
                    
            time.sleep(1)  # Short delay for demo
            
        self.wait_for_user()
        
    def scenario_4_multiple_failure_recovery(self):
        """Scenario 4: Multiple card failures and batch recovery"""
        self.print_banner("SCENARIO 4: Multiple Card Failures")
        
        self.print_step(1, "Simulating multiple failures")
        
        failures = {
            "nic-00": ("temperature_spike", 95.0),
            "nic-01": ("memory_corruption", 0),
            "nic-02": ("power_failure", 0)
        }
        
        for card_id, (failure_type, temp) in failures.items():
            card = self.system.cards[card_id]
            self.system.handle_failure_scenario(card, failure_type)
            if temp > 0:
                card.temperature = temp
                
        self.print_step(2, "System status after failures")
        self.show_card_status()
        self.wait_for_user()
        
        self.print_step(3, "Batch recovery procedure")
        recovery_results = {}
        
        for card_id in failures.keys():
            print(f"\nRecovering {card_id}...")
            success = self.system.recovery_procedure(card_id)
            recovery_results[card_id] = success
            time.sleep(0.5)  # Brief delay between recoveries
            
        self.print_step(4, "Recovery results")
        for card_id, success in recovery_results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"{card_id}: {status}")
            
        self.print_step(5, "Final system status")
        self.show_card_status()
        self.wait_for_user()
        
    def scenario_5_elasticsearch_integration(self):
        """Scenario 5: Elasticsearch logging and monitoring"""
        self.print_banner("SCENARIO 5: Elasticsearch Integration")
        
        self.print_step(1, "Checking Elasticsearch connectivity")
        es_available = self.system.check_elasticsearch_health()
        print(f"Elasticsearch available: {'✅ YES' if es_available else '❌ NO'}")
        
        if not es_available:
            print("Note: Elasticsearch not running. Events will be logged locally only.")
            
        self.wait_for_user()
        
        self.print_step(2, "Generating events for logging")
        
        events = [
            ("Install firmware", lambda: self.system.install_firmware("nic-00")),
            ("Health check", lambda: self.system.check_card_health("nic-01")),
            ("Anomaly detection", lambda: self.system.detect_anomalies("nic-02")),
            ("Tech support", lambda: self.system.generate_tech_support("nic-00"))
        ]
        
        for event_name, event_func in events:
            print(f"\nExecuting: {event_name}")
            try:
                event_func()
                print(f"✅ {event_name} completed")
            except Exception as e:
                print(f"❌ {event_name} failed: {e}")
            time.sleep(0.5)
            
        self.print_step(3, "Event logging summary")
        print("Events have been logged to:")
        print("- Local log file: /tmp/nic_firmware_mock.log")
        if es_available:
            print("- Elasticsearch indices: nic-firmware-YYYY.MM.DD")
        else:
            print("- Elasticsearch: Not available")
            
        self.wait_for_user()
        
    def run_interactive_demo(self):
        """Run interactive demo with user choices"""
        self.print_banner("NIC FIRMWARE MOCK SYSTEM - INTERACTIVE DEMO")
        
        scenarios = [
            ("Normal Firmware Installation", self.scenario_1_normal_installation),
            ("Installation Failure & Recovery", self.scenario_2_installation_failure),
            ("Health Monitoring & Alerts", self.scenario_3_health_monitoring),
            ("Multiple Card Failures", self.scenario_4_multiple_failure_recovery),
            ("Elasticsearch Integration", self.scenario_5_elasticsearch_integration)
        ]
        
        while True:
            print("\nAvailable Demo Scenarios:")
            print("0. Run all scenarios")
            for i, (name, _) in enumerate(scenarios, 1):
                print(f"{i}. {name}")
            print("q. Quit")
            
            choice = input("\nSelect scenario (0-5, q): ").strip().lower()
            
            if choice == 'q':
                print("Demo completed. Thank you!")
                break
            elif choice == '0':
                for name, scenario_func in scenarios:
                    scenario_func()
            elif choice.isdigit() and 1 <= int(choice) <= len(scenarios):
                _, scenario_func = scenarios[int(choice) - 1]
                scenario_func()
            else:
                print("Invalid choice. Please try again.")
                
    def run_automated_demo(self):
        """Run all scenarios automatically"""
        self.print_banner("NIC FIRMWARE MOCK SYSTEM - AUTOMATED DEMO")
        
        scenarios = [
            self.scenario_1_normal_installation,
            self.scenario_2_installation_failure,
            self.scenario_3_health_monitoring,
            self.scenario_4_multiple_failure_recovery,
            self.scenario_5_elasticsearch_integration
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n🚀 Running scenario {i}/{len(scenarios)}")
            scenario()
            if i < len(scenarios):
                print("\nMoving to next scenario in 3 seconds...")
                time.sleep(3)
                
        self.print_banner("ALL SCENARIOS COMPLETED")
        print("Demo finished successfully! 🎉")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="NIC Firmware Mock Demo Scenarios")
    parser.add_argument("--mode", choices=["interactive", "automated"], 
                       default="interactive", help="Demo mode")
    
    args = parser.parse_args()
    
    demo = DemoScenarios()
    
    if args.mode == "interactive":
        demo.run_interactive_demo()
    else:
        demo.run_automated_demo()

if __name__ == "__main__":
    main()
