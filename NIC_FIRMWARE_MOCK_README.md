# NIC Firmware Mock System

A comprehensive mock system for demonstrating NIC firmware installation, health monitoring, and recovery procedures for AMD Pensando DPUs.

## Overview

This mock system simulates the complete workflow of:
- Installing firmware on NIC cards
- Monitoring health status and detecting anomalies
- Handling failure scenarios with appropriate mitigation
- Capturing debug logs and technical support data
- Executing recovery procedures for faulty states

## Components

### 1. Core Mock System (`nic_firmware_mock.py`)
The main Python script that provides the core functionality:
- **Firmware Installation**: Simulates firmware upgrade process with progress tracking
- **Health Monitoring**: Monitors temperature, power consumption, link status, interrupts, and errors
- **Failure Scenarios**: Simulates realistic failure conditions (power failure, temperature spike, memory corruption, network timeout, checksum mismatch)
- **Recovery Procedures**: Multi-step recovery process to restore failed cards
- **Anomaly Detection**: Identifies abnormal conditions and alerts
- **Technical Support**: Generates comprehensive diagnostic bundles
- **Elasticsearch Integration**: Logs events to Elasticsearch for monitoring (when available)

### 2. CLI Commands Wrapper (`nic_cli_commands.sh`)
User-friendly command-line interface that provides:
- Colored output for better readability
- Interactive confirmations for destructive operations
- Additional utility commands (list, logs, reset, validate, benchmark)
- Error handling and status reporting

### 3. Demo Scenarios (`demo_scenarios.py`)
Interactive and automated demo system showcasing:
- Normal firmware installation workflow
- Installation failure and recovery procedures
- Continuous health monitoring with alerts
- Multiple card failure scenarios
- Elasticsearch integration testing

## Quick Start

### Prerequisites
- Python 3.8+
- Optional: Elasticsearch running on localhost:9200 for event logging

### Basic Usage

1. **Check system status:**
   ```bash
   ./nic_cli_commands.sh status
   ```

2. **Install firmware on a card:**
   ```bash
   ./nic_cli_commands.sh install nic-00
   ```

3. **Monitor card health:**
   ```bash
   ./nic_cli_commands.sh health
   ```

4. **Run recovery procedure:**
   ```bash
   ./nic_cli_commands.sh recovery nic-00
   ```

5. **Generate technical support bundle:**
   ```bash
   ./nic_cli_commands.sh techsupport nic-00
   ```

### Demo Mode

Run interactive demo:
```bash
python3 demo_scenarios.py --mode interactive
```

Run automated demo:
```bash
python3 demo_scenarios.py --mode automated
```

## Available Commands

### CLI Wrapper Commands
- `install <card_id>` - Install firmware on specified card
- `health [card_id]` - Check health status (all cards if no ID specified)
- `monitor` - Continuous monitoring of all cards
- `status [card_id]` - Show current status
- `recovery <card_id>` - Execute recovery procedure
- `techsupport <card_id>` - Generate technical support bundle
- `anomalies <card_id>` - Check for anomalies
- `list` - List all available cards
- `logs` - Show recent system logs
- `reset <card_id>` - Reset specified card
- `validate <card_id>` - Validate firmware integrity
- `benchmark <card_id>` - Run performance benchmark

### Python Script Commands
- `python3 nic_firmware_mock.py install <card_id>`
- `python3 nic_firmware_mock.py health [card_id]`
- `python3 nic_firmware_mock.py monitor`
- `python3 nic_firmware_mock.py recovery <card_id>`
- `python3 nic_firmware_mock.py techsupport <card_id>`
- `python3 nic_firmware_mock.py status [card_id]`
- `python3 nic_firmware_mock.py anomalies <card_id>`

## Failure Scenarios

The system simulates various realistic failure conditions:

1. **Power Failure** (5% probability)
   - Card becomes unresponsive
   - Link goes down
   - Status: FAILED, Health: CRITICAL

2. **Temperature Spike** (3% probability)
   - Temperature rises to 85-95°C
   - Health: WARNING or CRITICAL
   - May trigger thermal protection

3. **Memory Corruption** (2% probability)
   - Firmware becomes corrupted
   - High error count
   - Status: CORRUPTED, Health: CRITICAL

4. **Network Timeout** (4% probability)
   - Link connectivity issues
   - Increased interrupt count
   - Health: WARNING

5. **Checksum Mismatch** (3% probability)
   - Firmware integrity failure
   - Installation fails
   - Status: FAILED, Health: CRITICAL

## Recovery Procedures

The recovery system implements a 5-step process:

1. **Reset card hardware** - Hardware-level reset
2. **Load recovery firmware** - Load minimal recovery image
3. **Verify memory integrity** - Check for corruption
4. **Restore configuration** - Apply saved configuration
5. **Test basic functionality** - Validate operation

Recovery has a 10% failure rate to simulate real-world conditions.

## Monitoring and Alerting

### Health Metrics
- **Temperature**: 40-80°C normal range
- **Power Consumption**: 20-35W normal range
- **Link Status**: UP/DOWN
- **Interrupt Count**: Cumulative interrupts
- **Error Count**: Cumulative errors
- **Firmware Version**: Current and target versions

### Anomaly Detection
Automatically detects:
- High temperature (>80°C)
- Excessive errors (>20)
- High interrupt count (>100)
- Link down conditions
- High power consumption (>30W)

### Logging
- **Local Logs**: `/tmp/nic_firmware_mock.log`
- **Elasticsearch**: `nic-firmware-YYYY.MM.DD` indices
- **Tech Support**: `/tmp/techsupport_<card_id>_<timestamp>.txt`

## Integration with Pensando ELK

The mock system integrates with the existing Pensando ELK stack:
- Uses same Elasticsearch endpoint (localhost:9200)
- Follows similar logging patterns
- Compatible with existing monitoring dashboards
- Graceful fallback when Elasticsearch unavailable

## Environment Variables

- `ELASTICSEARCH_URL`: Elasticsearch endpoint (default: http://localhost:9200)
- `NIC_CARD_COUNT`: Number of cards to simulate (default: 2)

## Example Workflows

### Normal Installation
```bash
# Check initial status
./nic_cli_commands.sh status nic-00

# Install firmware
./nic_cli_commands.sh install nic-00

# Verify installation
./nic_cli_commands.sh health nic-00
```

### Failure Recovery
```bash
# Detect anomalies
./nic_cli_commands.sh anomalies nic-00

# Generate tech support
./nic_cli_commands.sh techsupport nic-00

# Execute recovery
./nic_cli_commands.sh recovery nic-00

# Validate recovery
./nic_cli_commands.sh validate nic-00
```

### Continuous Monitoring
```bash
# Start monitoring (Ctrl+C to stop)
./nic_cli_commands.sh monitor

# Or check logs
./nic_cli_commands.sh logs
```

## Technical Details

### Architecture
- **Object-oriented design** with clear separation of concerns
- **Enum-based status tracking** for type safety
- **JSON serialization** for API compatibility
- **Comprehensive logging** with multiple levels
- **Error handling** with graceful degradation

### Data Structures
- `NICCard`: Dataclass representing card state
- `FirmwareStatus`: Enum for installation status
- `HealthStatus`: Enum for health conditions
- `MockNICFirmwareSystem`: Main system controller

### Extensibility
- Easy to add new failure scenarios
- Configurable probability rates
- Pluggable recovery procedures
- Customizable health thresholds

## Testing

The system includes comprehensive testing through:
- Unit-level command testing
- Integration workflow testing
- Failure scenario validation
- Recovery procedure verification
- Demo scenario execution

Run all tests:
```bash
# Test basic functionality
python3 nic_firmware_mock.py status

# Test CLI wrapper
./nic_cli_commands.sh help

# Run demo scenarios
python3 demo_scenarios.py --mode automated
```

## Troubleshooting

### Common Issues

1. **Permission denied**: Ensure scripts are executable
   ```bash
   chmod +x nic_cli_commands.sh nic_firmware_mock.py demo_scenarios.py
   ```

2. **Python dependencies**: Install required packages
   ```bash
   pip3 install requests
   ```

3. **Elasticsearch connection**: Check if ELK stack is running
   ```bash
   curl http://localhost:9200/_health
   ```

### Log Files
- System logs: `/tmp/nic_firmware_mock.log`
- Tech support: `/tmp/techsupport_*.txt`

### Debug Mode
Enable verbose logging by modifying the logging level in the Python script.

## Future Enhancements

Potential improvements:
- Web-based dashboard for monitoring
- Integration with Grafana for visualization
- SNMP trap simulation
- Multi-node cluster simulation
- Performance benchmarking tools
- Configuration management
- Automated testing framework

## License

This mock system is provided as-is for demonstration purposes as part of the Pensando ELK project.
