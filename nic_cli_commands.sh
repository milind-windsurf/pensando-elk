#!/bin/bash


set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/nic_firmware_mock.py"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    print_status $RED "Error: Python script not found at $PYTHON_SCRIPT"
    exit 1
fi

show_help() {
    cat << EOF
NIC Firmware Management CLI Commands

USAGE:
    $0 <command> [options]

COMMANDS:
    install <card_id>           Install firmware on specified NIC card
    health [card_id]            Check health status (all cards if no ID specified)
    monitor                     Monitor all NIC cards continuously
    status [card_id]            Show current status (all cards if no ID specified)
    recovery <card_id>          Execute recovery procedure for failed card
    techsupport <card_id>       Generate technical support bundle
    anomalies <card_id>         Check for anomalies on specified card
    list                        List all available NIC cards
    logs                        Show recent system logs
    reset <card_id>             Reset specified NIC card
    validate <card_id>          Validate firmware integrity
    benchmark <card_id>         Run performance benchmark
    help                        Show this help message

EXAMPLES:
    $0 install nic-00           # Install firmware on nic-00
    $0 health                   # Check health of all cards
    $0 health nic-01            # Check health of specific card
    $0 recovery nic-00          # Recover failed card
    $0 techsupport nic-01       # Generate tech support for nic-01

ENVIRONMENT VARIABLES:
    ELASTICSEARCH_URL           Elasticsearch endpoint (default: http://localhost:9200)
    NIC_CARD_COUNT             Number of NIC cards to simulate (default: 2)

EOF
}

cmd_install() {
    local card_id=$1
    if [[ -z "$card_id" ]]; then
        print_status $RED "Error: Card ID required for install command"
        echo "Usage: $0 install <card_id>"
        exit 1
    fi
    
    print_status $BLUE "Installing firmware on $card_id..."
    python3 "$PYTHON_SCRIPT" install "$card_id"
    
    if [[ $? -eq 0 ]]; then
        print_status $GREEN "Firmware installation completed successfully"
    else
        print_status $RED "Firmware installation failed"
        exit 1
    fi
}

cmd_health() {
    local card_id=$1
    print_status $BLUE "Checking NIC card health..."
    
    if [[ -n "$card_id" ]]; then
        python3 "$PYTHON_SCRIPT" health "$card_id"
    else
        python3 "$PYTHON_SCRIPT" health
    fi
}

cmd_monitor() {
    print_status $BLUE "Monitoring NIC cards (Press Ctrl+C to stop)..."
    
    while true; do
        clear
        echo "=== NIC Card Monitoring Dashboard ==="
        echo "Updated: $(date)"
        echo "=================================="
        python3 "$PYTHON_SCRIPT" monitor
        echo ""
        print_status $YELLOW "Refreshing in 5 seconds..."
        sleep 5
    done
}

cmd_status() {
    local card_id=$1
    print_status $BLUE "Getting NIC card status..."
    
    if [[ -n "$card_id" ]]; then
        python3 "$PYTHON_SCRIPT" status "$card_id"
    else
        python3 "$PYTHON_SCRIPT" status
    fi
}

cmd_recovery() {
    local card_id=$1
    if [[ -z "$card_id" ]]; then
        print_status $RED "Error: Card ID required for recovery command"
        echo "Usage: $0 recovery <card_id>"
        exit 1
    fi
    
    print_status $YELLOW "WARNING: This will reset the NIC card and may cause temporary network disruption"
    read -p "Continue with recovery procedure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status $BLUE "Executing recovery procedure for $card_id..."
        python3 "$PYTHON_SCRIPT" recovery "$card_id"
        
        if [[ $? -eq 0 ]]; then
            print_status $GREEN "Recovery completed successfully"
        else
            print_status $RED "Recovery failed"
            exit 1
        fi
    else
        print_status $YELLOW "Recovery cancelled"
    fi
}

cmd_techsupport() {
    local card_id=$1
    if [[ -z "$card_id" ]]; then
        print_status $RED "Error: Card ID required for techsupport command"
        echo "Usage: $0 techsupport <card_id>"
        exit 1
    fi
    
    print_status $BLUE "Generating technical support bundle for $card_id..."
    python3 "$PYTHON_SCRIPT" techsupport "$card_id"
}

cmd_anomalies() {
    local card_id=$1
    if [[ -z "$card_id" ]]; then
        print_status $RED "Error: Card ID required for anomalies command"
        echo "Usage: $0 anomalies <card_id>"
        exit 1
    fi
    
    print_status $BLUE "Checking for anomalies on $card_id..."
    python3 "$PYTHON_SCRIPT" anomalies "$card_id"
}

cmd_list() {
    print_status $BLUE "Listing available NIC cards..."
    python3 "$PYTHON_SCRIPT" status | jq -r 'keys[]' 2>/dev/null || python3 "$PYTHON_SCRIPT" status | grep -o '"[^"]*":' | tr -d '":' | head -10
}

cmd_logs() {
    print_status $BLUE "Showing recent NIC firmware logs..."
    
    if [[ -f "/tmp/nic_firmware_mock.log" ]]; then
        tail -n 50 /tmp/nic_firmware_mock.log
    else
        print_status $YELLOW "No log file found. Run some commands first to generate logs."
    fi
}

cmd_reset() {
    local card_id=$1
    if [[ -z "$card_id" ]]; then
        print_status $RED "Error: Card ID required for reset command"
        echo "Usage: $0 reset <card_id>"
        exit 1
    fi
    
    print_status $YELLOW "WARNING: This will reset the NIC card"
    read -p "Continue with reset? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status $BLUE "Resetting $card_id..."
        python3 "$PYTHON_SCRIPT" recovery "$card_id"
        print_status $GREEN "Reset completed"
    else
        print_status $YELLOW "Reset cancelled"
    fi
}

cmd_validate() {
    local card_id=$1
    if [[ -z "$card_id" ]]; then
        print_status $RED "Error: Card ID required for validate command"
        echo "Usage: $0 validate <card_id>"
        exit 1
    fi
    
    print_status $BLUE "Validating firmware integrity for $card_id..."
    
    echo "Checking firmware checksum..."
    sleep 1
    echo "Verifying digital signature..."
    sleep 1
    echo "Testing basic functionality..."
    sleep 1
    
    status_output=$(python3 "$PYTHON_SCRIPT" status "$card_id" 2>/dev/null)
    
    if echo "$status_output" | grep -q '"status": "installed"'; then
        print_status $GREEN "Firmware validation PASSED"
    elif echo "$status_output" | grep -q '"status": "corrupted"'; then
        print_status $RED "Firmware validation FAILED - Corruption detected"
        exit 1
    else
        print_status $YELLOW "Firmware validation INCONCLUSIVE"
    fi
}

cmd_benchmark() {
    local card_id=$1
    if [[ -z "$card_id" ]]; then
        print_status $RED "Error: Card ID required for benchmark command"
        echo "Usage: $0 benchmark <card_id>"
        exit 1
    fi
    
    print_status $BLUE "Running performance benchmark for $card_id..."
    
    echo "Testing packet processing throughput..."
    sleep 2
    echo "Throughput: $(shuf -i 80-100 -n 1) Gbps"
    
    echo "Testing latency..."
    sleep 1
    echo "Latency: $(shuf -i 1-5 -n 1).$(shuf -i 0-9 -n 1) μs"
    
    echo "Testing memory bandwidth..."
    sleep 1
    echo "Memory bandwidth: $(shuf -i 200-250 -n 1) GB/s"
    
    echo "Testing CPU utilization..."
    sleep 1
    echo "CPU utilization: $(shuf -i 15-35 -n 1)%"
    
    print_status $GREEN "Benchmark completed successfully"
}

case "${1:-help}" in
    install)
        cmd_install "$2"
        ;;
    health)
        cmd_health "$2"
        ;;
    monitor)
        cmd_monitor
        ;;
    status)
        cmd_status "$2"
        ;;
    recovery)
        cmd_recovery "$2"
        ;;
    techsupport)
        cmd_techsupport "$2"
        ;;
    anomalies)
        cmd_anomalies "$2"
        ;;
    list)
        cmd_list
        ;;
    logs)
        cmd_logs
        ;;
    reset)
        cmd_reset "$2"
        ;;
    validate)
        cmd_validate "$2"
        ;;
    benchmark)
        cmd_benchmark "$2"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_status $RED "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
