# NIC Firmware Installation Automation

This automation framework provides comprehensive NIC firmware installation with health verification, failure handling, debug logging, and recovery mechanisms for AMD Pensando DPU environments.

## Features

### 🔍 Health Verification
- **Interrupt Monitoring**: Detects interrupt storms and anomalies
- **Core Dump Detection**: Identifies and analyzes core dumps
- **Alert Monitoring**: Tracks system alerts and warnings
- **Event Analysis**: Monitors system events related to NIC operations
- **Anomaly Detection**: Identifies performance and behavioral anomalies

### 🛠️ Failure Scenario Handling
- **Boot Failures**: NIC fails to boot after firmware installation
- **Driver Issues**: Driver compatibility problems
- **Hardware Faults**: Physical hardware problems
- **Firmware Corruption**: Corrupted firmware images
- **Network Connectivity**: Network connectivity issues
- **Interrupt Storms**: Excessive interrupt generation
- **Core Dumps**: System crashes and core dumps
- **Memory Leaks**: Memory leak detection and handling

### 🐛 Debug and Logging
- **Comprehensive Logging**: Detailed logging with configurable levels
- **Debug Data Capture**: Captures system state for analysis
- **Techsupport Generation**: Creates comprehensive support bundles
- **Log Aggregation**: Integrates with existing ELK stack

### 🔧 Recovery Mechanisms
- **Recovery Recipes**: Predefined recovery procedures for each failure type
- **Automatic Rollback**: Firmware rollback capabilities
- **Service Recovery**: Automatic service restart and recovery
- **Hardware Reset**: Hardware reset procedures

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements_automation.txt
   ```

2. **Configure the System**:
   ```bash
   # Create necessary directories
   sudo mkdir -p /var/log/nic_automation
   sudo mkdir -p /var/log/techsupport
   sudo mkdir -p /opt/firmware/backup
   
   # Set permissions
   sudo chown -R $USER:$USER /var/log/nic_automation
   sudo chown -R $USER:$USER /var/log/techsupport
   ```

3. **Copy Configuration**:
   ```bash
   cp config/nic_automation_config.json /etc/nic_automation_config.json
   ```

## Usage

### Command Line Interface

The automation provides a comprehensive CLI for all operations:

```bash
# Install firmware with full automation
python cli_integration.py install /path/to/firmware.bin

# Run health checks
python cli_integration.py health

# Execute recovery for specific failure
python cli_integration.py recover boot_failure

# Capture debug information
python cli_integration.py debug --output debug_data.json

# Show system status
python cli_integration.py status

# List available failure scenarios
python cli_integration.py scenarios

# Execute specific recovery recipe
python cli_integration.py recipe boot_failure_recovery

# Run test suite
python cli_integration.py test
```

### Python API

```python
from nic_firmware_automation import NICFirmwareAutomation, FailureType

# Create automation instance
automation = NICFirmwareAutomation("config.json")

# Install firmware
success = automation.run_automation("/path/to/firmware.bin")

# Run health checks
health_checks = automation.run_comprehensive_health_check()

# Handle specific failure
automation.handle_failure_scenario(FailureType.BOOT_FAILURE)

# Capture debug data
debug_data = automation.capture_debug_logs()

# Generate techsupport
techsupport_path = automation.generate_techsupport()
```

## Configuration

The automation is configured via JSON configuration file:

```json
{
  "nic_interface": "eth0",
  "firmware_path": "/opt/firmware/",
  "backup_path": "/opt/firmware/backup/",
  "log_path": "/var/log/nic_automation/",
  "cli_timeout": 30,
  "health_check_interval": 5,
  "max_recovery_attempts": 3,
  "debug_mode": true,
  "techsupport_path": "/var/log/techsupport/"
}
```

## Health Checks

The automation performs comprehensive health checks:

### Interrupt Check
- Monitors interrupt rates and patterns
- Detects interrupt storms
- Checks interrupt affinity

### Core Dump Check
- Scans for core dump files
- Analyzes core dump timestamps
- Identifies recurring crashes

### Alert Check
- Monitors system alerts
- Categorizes alert severity
- Tracks alert trends

### Event Check
- Analyzes system events
- Filters NIC-related events
- Identifies error patterns

### Anomaly Check
- Monitors network statistics
- Detects performance anomalies
- Identifies packet loss patterns

## Failure Scenarios

The automation handles various failure scenarios:

| Failure Type | Description | Severity | Recovery Recipe |
|--------------|-------------|----------|-----------------|
| Boot Failure | NIC fails to boot after firmware installation | Critical | boot_failure_recovery |
| Driver Issue | Driver compatibility issues | High | driver_recovery |
| Hardware Fault | Hardware fault detected | Critical | hardware_fault_recovery |
| Firmware Corruption | Firmware image corruption | High | firmware_corruption_recovery |
| Network Connectivity | Network connectivity lost | Medium | network_recovery |
| Interrupt Storm | Excessive interrupts detected | High | interrupt_storm_recovery |
| Core Dump | Core dump detected | High | core_dump_recovery |
| Memory Leak | Memory leak detected | Medium | memory_leak_recovery |

## Recovery Recipes

Each failure scenario has a corresponding recovery recipe:

### Boot Failure Recovery
1. Reset NIC to factory defaults
2. Reload firmware from backup
3. Restart system services
4. Verify basic connectivity

### Driver Recovery
1. Unload NIC driver modules
2. Reload driver modules
3. Restart network services
4. Verify driver functionality

### Hardware Fault Recovery
1. Run hardware diagnostics
2. Reset hardware components
3. Check physical connections
4. Escalate to hardware team if needed

## Integration with ELK Stack

The automation integrates with the existing ELK stack for log aggregation and analysis:

- **Logstash**: Processes automation logs
- **Elasticsearch**: Stores automation data
- **Kibana**: Visualizes automation metrics

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python test_nic_automation.py

# Run specific test via CLI
python cli_integration.py test
```

Test scenarios include:
- Successful firmware installation
- Various failure scenarios
- Health check functionality
- Debug logging and techsupport
- Recovery recipe execution

## Monitoring and Alerting

The automation provides monitoring capabilities:

- **Real-time Health Monitoring**: Continuous health checks
- **Alert Generation**: Configurable alerting for failures
- **Metrics Collection**: Performance and health metrics
- **Dashboard Integration**: Kibana dashboard integration

## Troubleshooting

### Common Issues

1. **Permission Errors**:
   ```bash
   sudo chown -R $USER:$USER /var/log/nic_automation
   ```

2. **Missing Dependencies**:
   ```bash
   pip install -r requirements_automation.txt
   ```

3. **Configuration Issues**:
   - Verify configuration file syntax
   - Check file paths and permissions
   - Validate NIC interface names

### Debug Mode

Enable debug mode for detailed logging:

```bash
python cli_integration.py --debug install firmware.bin
```

### Log Analysis

Check automation logs:

```bash
tail -f /var/log/nic_automation/nic_automation_*.log
```

## Support

For issues and questions:

1. Check the automation logs
2. Run debug data capture
3. Generate techsupport bundle
4. Review health check results

## License

This automation framework is released under the same license as the pensando-elk project.
