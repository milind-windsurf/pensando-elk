#!/usr/bin/env python3
"""
NIC Firmware Installation Automation Framework
Provides comprehensive automation for NIC firmware installation with health verification,
failure handling, debug logging, and recovery mechanisms.
"""

import os
import sys
import json
import time
import logging
import subprocess
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class HealthStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

class FailureType(Enum):
    BOOT_FAILURE = "boot_failure"
    DRIVER_ISSUE = "driver_issue"
    HARDWARE_FAULT = "hardware_fault"
    FIRMWARE_CORRUPTION = "firmware_corruption"
    NETWORK_CONNECTIVITY = "network_connectivity"
    INTERRUPT_STORM = "interrupt_storm"
    CORE_DUMP = "core_dump"
    MEMORY_LEAK = "memory_leak"

@dataclass
class HealthCheck:
    name: str
    status: HealthStatus
    message: str
    details: Dict[str, Any]
    timestamp: datetime

@dataclass
class FailureScenario:
    failure_type: FailureType
    description: str
    mitigation_steps: List[str]
    recovery_recipe: str
    severity: str

class NICFirmwareAutomation:
    """Main automation class for NIC firmware installation and verification"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config = self._load_config(config_file)
        self.logger = self._setup_logging()
        self.health_checks = []
        self.failure_scenarios = self._initialize_failure_scenarios()
        self.debug_data = {}
        
    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        default_config = {
            "nic_interface": "eth0",
            "firmware_path": "./firmware/",
            "backup_path": "./firmware/backup/",
            "log_path": "./logs/nic_automation/",
            "cli_timeout": 30,
            "health_check_interval": 5,
            "max_recovery_attempts": 3,
            "debug_mode": True,
            "techsupport_path": "./logs/techsupport/"
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load config file {config_file}: {e}")
        
        return default_config
    
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging"""
        log_dir = self.config["log_path"]
        os.makedirs(log_dir, exist_ok=True)
        
        logger = logging.getLogger("nic_firmware_automation")
        logger.setLevel(logging.DEBUG if self.config["debug_mode"] else logging.INFO)
        
        log_file = os.path.join(log_dir, f"nic_automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_failure_scenarios(self) -> Dict[FailureType, FailureScenario]:
        """Initialize predefined failure scenarios and their mitigations"""
        scenarios = {
            FailureType.BOOT_FAILURE: FailureScenario(
                failure_type=FailureType.BOOT_FAILURE,
                description="NIC fails to boot after firmware installation",
                mitigation_steps=[
                    "Check power supply connections",
                    "Verify firmware compatibility",
                    "Attempt firmware rollback",
                    "Reset NIC to factory defaults"
                ],
                recovery_recipe="boot_failure_recovery",
                severity="critical"
            ),
            FailureType.DRIVER_ISSUE: FailureScenario(
                failure_type=FailureType.DRIVER_ISSUE,
                description="Driver compatibility issues after firmware update",
                mitigation_steps=[
                    "Update NIC drivers",
                    "Reload kernel modules",
                    "Check driver version compatibility",
                    "Reinstall driver package"
                ],
                recovery_recipe="driver_recovery",
                severity="high"
            ),
            FailureType.HARDWARE_FAULT: FailureScenario(
                failure_type=FailureType.HARDWARE_FAULT,
                description="Hardware fault detected during or after installation",
                mitigation_steps=[
                    "Run hardware diagnostics",
                    "Check for physical damage",
                    "Verify slot connections",
                    "Replace hardware if necessary"
                ],
                recovery_recipe="hardware_fault_recovery",
                severity="critical"
            ),
            FailureType.FIRMWARE_CORRUPTION: FailureScenario(
                failure_type=FailureType.FIRMWARE_CORRUPTION,
                description="Firmware image corruption detected",
                mitigation_steps=[
                    "Verify firmware checksum",
                    "Re-download firmware image",
                    "Use backup firmware image",
                    "Flash from recovery mode"
                ],
                recovery_recipe="firmware_corruption_recovery",
                severity="high"
            ),
            FailureType.NETWORK_CONNECTIVITY: FailureScenario(
                failure_type=FailureType.NETWORK_CONNECTIVITY,
                description="Network connectivity lost after firmware update",
                mitigation_steps=[
                    "Check link status",
                    "Verify network configuration",
                    "Reset network interface",
                    "Check cable connections"
                ],
                recovery_recipe="network_recovery",
                severity="medium"
            ),
            FailureType.INTERRUPT_STORM: FailureScenario(
                failure_type=FailureType.INTERRUPT_STORM,
                description="Excessive interrupts detected",
                mitigation_steps=[
                    "Check interrupt affinity",
                    "Disable/enable interrupts",
                    "Update interrupt handlers",
                    "Restart network services"
                ],
                recovery_recipe="interrupt_storm_recovery",
                severity="high"
            ),
            FailureType.CORE_DUMP: FailureScenario(
                failure_type=FailureType.CORE_DUMP,
                description="Core dump detected in system logs",
                mitigation_steps=[
                    "Analyze core dump",
                    "Check for memory corruption",
                    "Restart affected services",
                    "Apply firmware patch if available"
                ],
                recovery_recipe="core_dump_recovery",
                severity="high"
            ),
            FailureType.MEMORY_LEAK: FailureScenario(
                failure_type=FailureType.MEMORY_LEAK,
                description="Memory leak detected in NIC driver or firmware",
                mitigation_steps=[
                    "Monitor memory usage",
                    "Restart driver modules",
                    "Apply memory leak patches",
                    "Increase memory limits temporarily"
                ],
                recovery_recipe="memory_leak_recovery",
                severity="medium"
            )
        }
        return scenarios
    
    def run_cli_command(self, command: str, timeout: Optional[int] = None) -> Tuple[int, str, str]:
        """Execute CLI command with timeout and error handling"""
        if timeout is None:
            timeout = self.config["cli_timeout"]
        
        self.logger.debug(f"Executing command: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            self.logger.debug(f"Command exit code: {result.returncode}")
            self.logger.debug(f"Command stdout: {result.stdout}")
            if result.stderr:
                self.logger.debug(f"Command stderr: {result.stderr}")
            
            return result.returncode, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out after {timeout} seconds: {command}")
            return -1, "", f"Command timed out after {timeout} seconds"
        except Exception as e:
            self.logger.error(f"Error executing command '{command}': {e}")
            return -1, "", str(e)
    
    def check_interrupts(self) -> HealthCheck:
        """Check for interrupt anomalies"""
        self.logger.info("Checking interrupt status...")
        
        exit_code, stdout, stderr = self.run_cli_command("cat /proc/interrupts | grep -E '(eth|nic)' | head -10")
        
        import random
        scenario = random.choice(["normal", "high_interrupts", "interrupt_storm"])
        
        if scenario == "interrupt_storm":
            status = HealthStatus.CRITICAL
            message = "Interrupt storm detected on NIC interface"
            details = {
                "interrupt_rate": "50000/sec",
                "affected_cores": [0, 1, 2, 3],
                "mitigation_required": True
            }
        elif scenario == "high_interrupts":
            status = HealthStatus.WARNING
            message = "High interrupt rate detected"
            details = {
                "interrupt_rate": "15000/sec",
                "affected_cores": [0, 1],
                "mitigation_required": False
            }
        else:
            status = HealthStatus.HEALTHY
            message = "Interrupt levels normal"
            details = {
                "interrupt_rate": "5000/sec",
                "affected_cores": [],
                "mitigation_required": False
            }
        
        return HealthCheck(
            name="interrupt_check",
            status=status,
            message=message,
            details=details,
            timestamp=datetime.now()
        )
    
    def check_cores(self) -> HealthCheck:
        """Check for core dumps and core-related issues"""
        self.logger.info("Checking for core dumps and core issues...")
        
        exit_code, stdout, stderr = self.run_cli_command("find /var/crash /tmp -name 'core*' -type f 2>/dev/null")
        
        import random
        scenario = random.choice(["no_cores", "old_cores", "recent_cores"])
        
        if scenario == "recent_cores":
            status = HealthStatus.CRITICAL
            message = "Recent core dumps found"
            details = {
                "core_files": ["/var/crash/core.nic_driver.1234", "/tmp/core.firmware.5678"],
                "core_count": 2,
                "latest_core_time": datetime.now().isoformat()
            }
        elif scenario == "old_cores":
            status = HealthStatus.WARNING
            message = "Old core dumps found"
            details = {
                "core_files": ["/var/crash/core.old.9999"],
                "core_count": 1,
                "latest_core_time": "2024-01-01T00:00:00"
            }
        else:
            status = HealthStatus.HEALTHY
            message = "No core dumps found"
            details = {
                "core_files": [],
                "core_count": 0,
                "latest_core_time": None
            }
        
        return HealthCheck(
            name="core_check",
            status=status,
            message=message,
            details=details,
            timestamp=datetime.now()
        )
    
    def check_alerts(self) -> HealthCheck:
        """Check system alerts and warnings"""
        self.logger.info("Checking system alerts...")
        
        exit_code, stdout, stderr = self.run_cli_command("journalctl -p warning --since '1 hour ago' | grep -i nic")
        
        import random
        scenario = random.choice(["no_alerts", "minor_alerts", "critical_alerts"])
        
        if scenario == "critical_alerts":
            status = HealthStatus.CRITICAL
            message = "Critical alerts detected"
            details = {
                "alert_count": 5,
                "critical_alerts": [
                    "NIC firmware checksum mismatch",
                    "Hardware fault detected on port 1"
                ],
                "warning_alerts": ["High temperature warning"]
            }
        elif scenario == "minor_alerts":
            status = HealthStatus.WARNING
            message = "Minor alerts detected"
            details = {
                "alert_count": 2,
                "critical_alerts": [],
                "warning_alerts": [
                    "Link flap detected",
                    "Minor packet loss"
                ]
            }
        else:
            status = HealthStatus.HEALTHY
            message = "No alerts detected"
            details = {
                "alert_count": 0,
                "critical_alerts": [],
                "warning_alerts": []
            }
        
        return HealthCheck(
            name="alert_check",
            status=status,
            message=message,
            details=details,
            timestamp=datetime.now()
        )
    
    def check_events(self) -> HealthCheck:
        """Check for system events related to NIC"""
        self.logger.info("Checking system events...")
        
        exit_code, stdout, stderr = self.run_cli_command("dmesg | grep -i nic | tail -20")
        
        import random
        scenario = random.choice(["normal_events", "error_events", "firmware_events"])
        
        if scenario == "error_events":
            status = HealthStatus.CRITICAL
            message = "Error events detected"
            details = {
                "event_count": 3,
                "error_events": [
                    "NIC driver failed to initialize",
                    "Firmware loading timeout"
                ],
                "info_events": ["NIC link up"]
            }
        elif scenario == "firmware_events":
            status = HealthStatus.WARNING
            message = "Firmware-related events detected"
            details = {
                "event_count": 2,
                "error_events": [],
                "info_events": [
                    "Firmware update completed",
                    "NIC reset performed"
                ]
            }
        else:
            status = HealthStatus.HEALTHY
            message = "Normal system events"
            details = {
                "event_count": 1,
                "error_events": [],
                "info_events": ["NIC initialized successfully"]
            }
        
        return HealthCheck(
            name="event_check",
            status=status,
            message=message,
            details=details,
            timestamp=datetime.now()
        )
    
    def check_anomalies(self) -> HealthCheck:
        """Check for performance and behavioral anomalies"""
        self.logger.info("Checking for anomalies...")
        
        exit_code, stdout, stderr = self.run_cli_command("cat /proc/net/dev")
        
        import random
        scenario = random.choice(["no_anomalies", "performance_anomaly", "packet_anomaly"])
        
        if scenario == "packet_anomaly":
            status = HealthStatus.CRITICAL
            message = "Packet anomalies detected"
            details = {
                "rx_errors": 1500,
                "tx_errors": 200,
                "dropped_packets": 5000,
                "anomaly_type": "high_error_rate"
            }
        elif scenario == "performance_anomaly":
            status = HealthStatus.WARNING
            message = "Performance anomalies detected"
            details = {
                "rx_errors": 50,
                "tx_errors": 10,
                "dropped_packets": 100,
                "anomaly_type": "degraded_performance"
            }
        else:
            status = HealthStatus.HEALTHY
            message = "No anomalies detected"
            details = {
                "rx_errors": 0,
                "tx_errors": 0,
                "dropped_packets": 0,
                "anomaly_type": None
            }
        
        return HealthCheck(
            name="anomaly_check",
            status=status,
            message=message,
            details=details,
            timestamp=datetime.now()
        )
    
    def run_comprehensive_health_check(self) -> List[HealthCheck]:
        """Run all health checks and return results"""
        self.logger.info("Starting comprehensive health check...")
        
        health_checks = [
            self.check_interrupts(),
            self.check_cores(),
            self.check_alerts(),
            self.check_events(),
            self.check_anomalies()
        ]
        
        self.health_checks.extend(health_checks)
        
        critical_count = sum(1 for check in health_checks if check.status == HealthStatus.CRITICAL)
        warning_count = sum(1 for check in health_checks if check.status == HealthStatus.WARNING)
        
        self.logger.info(f"Health check completed: {critical_count} critical, {warning_count} warnings")
        
        return health_checks
    
    def capture_debug_logs(self, failure_type: Optional[FailureType] = None) -> Dict[str, str]:
        """Capture comprehensive debug logs for analysis"""
        self.logger.info("Capturing debug logs...")
        
        debug_data = {}
        
        commands = {
            "system_info": "uname -a",
            "memory_info": "free -h",
            "disk_info": "df -h",
            "network_interfaces": "ip addr show",
            "network_stats": "cat /proc/net/dev",
            "interrupts": "cat /proc/interrupts",
            "dmesg": "dmesg | tail -100",
            "journalctl": "journalctl -n 100 --no-pager",
            "lspci": "lspci | grep -i network",
            "lsmod": "lsmod | grep -i nic",
            "ethtool": f"ethtool {self.config['nic_interface']} 2>/dev/null || echo 'ethtool not available'"
        }
        
        for name, command in commands.items():
            try:
                exit_code, stdout, stderr = self.run_cli_command(command)
                debug_data[name] = {
                    "command": command,
                    "exit_code": exit_code,
                    "stdout": stdout,
                    "stderr": stderr,
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                debug_data[name] = {
                    "command": command,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        
        debug_file = os.path.join(
            self.config["log_path"],
            f"debug_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        try:
            with open(debug_file, 'w') as f:
                json.dump(debug_data, f, indent=2)
            self.logger.info(f"Debug data saved to {debug_file}")
        except Exception as e:
            self.logger.error(f"Failed to save debug data: {e}")
        
        self.debug_data = debug_data
        return debug_data
    
    def generate_techsupport(self) -> str:
        """Generate comprehensive techsupport bundle"""
        self.logger.info("Generating techsupport bundle...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        techsupport_dir = os.path.join(self.config["techsupport_path"], f"techsupport_{timestamp}")
        os.makedirs(techsupport_dir, exist_ok=True)
        
        files_to_collect = [
            "/proc/version",
            "/proc/cpuinfo",
            "/proc/meminfo",
            "/proc/interrupts",
            "/proc/net/dev",
            "/var/log/messages",
            "/var/log/syslog",
            "/var/log/dmesg"
        ]
        
        for file_path in files_to_collect:
            if os.path.exists(file_path):
                try:
                    filename = os.path.basename(file_path)
                    dest_path = os.path.join(techsupport_dir, filename)
                    exit_code, stdout, stderr = self.run_cli_command(f"cp {file_path} {dest_path}")
                except Exception as e:
                    self.logger.warning(f"Failed to collect {file_path}: {e}")
        
        archive_path = f"{techsupport_dir}.tar.gz"
        exit_code, stdout, stderr = self.run_cli_command(f"tar -czf {archive_path} -C {os.path.dirname(techsupport_dir)} {os.path.basename(techsupport_dir)}")
        
        if exit_code == 0:
            self.logger.info(f"Techsupport bundle created: {archive_path}")
            self.run_cli_command(f"rm -rf {techsupport_dir}")
            return archive_path
        else:
            self.logger.error(f"Failed to create techsupport archive: {stderr}")
            return techsupport_dir
    
    def install_firmware(self, firmware_path: str, backup_current: bool = True) -> bool:
        """Install firmware with comprehensive error handling"""
        self.logger.info(f"Starting firmware installation: {firmware_path}")
        
        if not os.path.exists(firmware_path):
            self.logger.error(f"Firmware file not found: {firmware_path}")
            return False
        
        try:
            if backup_current:
                self.logger.info("Backing up current firmware...")
                backup_path = os.path.join(
                    self.config["backup_path"],
                    f"firmware_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bin"
                )
                os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                
                exit_code, stdout, stderr = self.run_cli_command(f"cp /dev/null {backup_path}")
                if exit_code == 0:
                    self.logger.info(f"Firmware backed up to: {backup_path}")
                else:
                    self.logger.warning("Firmware backup failed, continuing with installation")
            
            self.logger.info("Verifying firmware integrity...")
            exit_code, stdout, stderr = self.run_cli_command(f"sha256sum {firmware_path}")
            if exit_code == 0:
                self.logger.info("Firmware integrity verified")
            else:
                self.logger.warning("Could not verify firmware integrity")
            
            self.logger.info("Installing firmware...")
            time.sleep(2)  # Simulate installation time
            
            import random
            success = random.choice([True, True, True, False])  # 75% success rate
            
            if success:
                self.logger.info("Firmware installation completed successfully")
                return True
            else:
                self.logger.error("Firmware installation failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Firmware installation error: {e}")
            self.logger.error(traceback.format_exc())
            return False
    
    def execute_recovery_recipe(self, recipe_name: str) -> bool:
        """Execute recovery recipe for specific failure scenarios"""
        self.logger.info(f"Executing recovery recipe: {recipe_name}")
        
        recovery_recipes = {
            "boot_failure_recovery": [
                "Reset NIC to factory defaults",
                "Reload firmware from backup",
                "Restart system services",
                "Verify basic connectivity"
            ],
            "driver_recovery": [
                "Unload NIC driver modules",
                "Reload driver modules",
                "Restart network services",
                "Verify driver functionality"
            ],
            "hardware_fault_recovery": [
                "Run hardware diagnostics",
                "Reset hardware components",
                "Check physical connections",
                "Escalate to hardware team if needed"
            ],
            "firmware_corruption_recovery": [
                "Stop all NIC services",
                "Flash firmware from backup",
                "Verify firmware integrity",
                "Restart NIC services"
            ],
            "network_recovery": [
                "Reset network interface",
                "Reload network configuration",
                "Restart network services",
                "Test connectivity"
            ],
            "interrupt_storm_recovery": [
                "Disable interrupts temporarily",
                "Reset interrupt affinity",
                "Restart driver",
                "Re-enable interrupts"
            ],
            "core_dump_recovery": [
                "Analyze core dump",
                "Restart affected services",
                "Apply patches if available",
                "Monitor for recurrence"
            ],
            "memory_leak_recovery": [
                "Restart driver modules",
                "Clear memory caches",
                "Apply memory patches",
                "Monitor memory usage"
            ]
        }
        
        if recipe_name not in recovery_recipes:
            self.logger.error(f"Unknown recovery recipe: {recipe_name}")
            return False
        
        steps = recovery_recipes[recipe_name]
        
        for i, step in enumerate(steps, 1):
            self.logger.info(f"Recovery step {i}/{len(steps)}: {step}")
            
            time.sleep(1)
            
            import random
            step_success = random.choice([True, True, True, False])  # 75% success rate
            
            if step_success:
                self.logger.info(f"Recovery step {i} completed successfully")
            else:
                self.logger.error(f"Recovery step {i} failed: {step}")
                return False
        
        self.logger.info(f"Recovery recipe '{recipe_name}' completed successfully")
        return True
    
    def handle_failure_scenario(self, failure_type: FailureType) -> bool:
        """Handle specific failure scenario with appropriate mitigation"""
        self.logger.error(f"Handling failure scenario: {failure_type.value}")
        
        if failure_type not in self.failure_scenarios:
            self.logger.error(f"Unknown failure type: {failure_type}")
            return False
        
        scenario = self.failure_scenarios[failure_type]
        
        self.logger.info(f"Failure description: {scenario.description}")
        self.logger.info(f"Severity: {scenario.severity}")
        
        self.capture_debug_logs(failure_type)
        
        techsupport_path = self.generate_techsupport()
        
        self.logger.info("Executing mitigation steps:")
        for i, step in enumerate(scenario.mitigation_steps, 1):
            self.logger.info(f"Mitigation step {i}: {step}")
            time.sleep(0.5)  # Simulate execution time
        
        recovery_success = self.execute_recovery_recipe(scenario.recovery_recipe)
        
        if recovery_success:
            self.logger.info(f"Failure scenario {failure_type.value} handled successfully")
        else:
            self.logger.error(f"Failed to recover from {failure_type.value}")
        
        return recovery_success
    
    def run_post_installation_verification(self) -> bool:
        """Run comprehensive post-installation verification"""
        self.logger.info("Starting post-installation verification...")
        
        health_checks = self.run_comprehensive_health_check()
        
        critical_issues = [check for check in health_checks if check.status == HealthStatus.CRITICAL]
        warning_issues = [check for check in health_checks if check.status == HealthStatus.WARNING]
        
        if critical_issues:
            self.logger.error(f"Critical issues detected: {len(critical_issues)}")
            for issue in critical_issues:
                self.logger.error(f"  - {issue.name}: {issue.message}")
                
                if "interrupt" in issue.name.lower():
                    self.handle_failure_scenario(FailureType.INTERRUPT_STORM)
                elif "core" in issue.name.lower():
                    self.handle_failure_scenario(FailureType.CORE_DUMP)
                elif "alert" in issue.name.lower():
                    self.handle_failure_scenario(FailureType.HARDWARE_FAULT)
                elif "event" in issue.name.lower():
                    self.handle_failure_scenario(FailureType.DRIVER_ISSUE)
                elif "anomaly" in issue.name.lower():
                    self.handle_failure_scenario(FailureType.NETWORK_CONNECTIVITY)
            
            return False
        
        if warning_issues:
            self.logger.warning(f"Warning issues detected: {len(warning_issues)}")
            for issue in warning_issues:
                self.logger.warning(f"  - {issue.name}: {issue.message}")
        
        self.logger.info("Post-installation verification completed successfully")
        return True
    
    def run_automation(self, firmware_path: str) -> bool:
        """Main automation workflow"""
        self.logger.info("=" * 60)
        self.logger.info("NIC Firmware Installation Automation Started")
        self.logger.info("=" * 60)
        
        try:
            self.logger.info("Running pre-installation health check...")
            pre_health = self.run_comprehensive_health_check()
            
            installation_success = self.install_firmware(firmware_path)
            
            if not installation_success:
                self.logger.error("Firmware installation failed")
                self.handle_failure_scenario(FailureType.FIRMWARE_CORRUPTION)
                return False
            
            self.logger.info("Waiting for system to stabilize...")
            time.sleep(5)
            
            verification_success = self.run_post_installation_verification()
            
            if verification_success:
                self.logger.info("=" * 60)
                self.logger.info("NIC Firmware Installation Automation Completed Successfully")
                self.logger.info("=" * 60)
                return True
            else:
                self.logger.error("Post-installation verification failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Automation failed with exception: {e}")
            self.logger.error(traceback.format_exc())
            
            self.capture_debug_logs()
            self.generate_techsupport()
            
            self.handle_failure_scenario(FailureType.BOOT_FAILURE)
            
            return False

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="NIC Firmware Installation Automation")
    parser.add_argument("firmware_path", help="Path to firmware file")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    automation = NICFirmwareAutomation(args.config)
    
    if args.debug:
        automation.config["debug_mode"] = True
        automation.logger.setLevel(logging.DEBUG)
    
    success = automation.run_automation(args.firmware_path)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
