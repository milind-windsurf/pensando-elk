#!/usr/bin/env python3
"""
CLI Integration Module for NIC Firmware Automation
Provides command-line interface and integration with existing monitoring tools
"""

import os
import sys
import json
import click
import tabulate
from datetime import datetime
from typing import List, Dict, Any, Optional

from nic_firmware_automation import (
    NICFirmwareAutomation, 
    HealthStatus, 
    FailureType,
    HealthCheck
)

class CLIIntegration:
    """CLI integration for NIC firmware automation"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.automation = NICFirmwareAutomation(config_file)
    
    def format_health_check_table(self, health_checks: List[HealthCheck]) -> str:
        """Format health checks as a table"""
        headers = ["Check Name", "Status", "Message", "Timestamp"]
        rows = []
        
        for check in health_checks:
            status_color = {
                HealthStatus.HEALTHY: "✅",
                HealthStatus.WARNING: "⚠️",
                HealthStatus.CRITICAL: "❌",
                HealthStatus.UNKNOWN: "❓"
            }.get(check.status, "❓")
            
            rows.append([
                check.name,
                f"{status_color} {check.status.value}",
                check.message[:50] + "..." if len(check.message) > 50 else check.message,
                check.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            ])
        
        return tabulate.tabulate(rows, headers=headers, tablefmt="grid")
    
    def format_failure_scenarios_table(self) -> str:
        """Format failure scenarios as a table"""
        headers = ["Failure Type", "Description", "Severity", "Recovery Recipe"]
        rows = []
        
        for failure_type, scenario in self.automation.failure_scenarios.items():
            rows.append([
                failure_type.value,
                scenario.description[:40] + "..." if len(scenario.description) > 40 else scenario.description,
                scenario.severity,
                scenario.recovery_recipe
            ])
        
        return tabulate.tabulate(rows, headers=headers, tablefmt="grid")

@click.group()
@click.option('--config', '-c', help='Configuration file path')
@click.option('--debug', '-d', is_flag=True, help='Enable debug mode')
@click.pass_context
def cli(ctx, config, debug):
    """NIC Firmware Installation Automation CLI"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['debug'] = debug

@cli.command()
@click.argument('firmware_path')
@click.option('--backup/--no-backup', default=True, help='Backup current firmware')
@click.pass_context
def install(ctx, firmware_path, backup):
    """Install firmware with comprehensive verification"""
    click.echo("🚀 Starting NIC firmware installation automation...")
    
    automation = NICFirmwareAutomation(ctx.obj['config'])
    if ctx.obj['debug']:
        automation.config['debug_mode'] = True
    
    if not os.path.exists(firmware_path):
        click.echo(f"❌ Error: Firmware file not found: {firmware_path}", err=True)
        sys.exit(1)
    
    success = automation.run_automation(firmware_path)
    
    if success:
        click.echo("✅ Firmware installation completed successfully!")
        sys.exit(0)
    else:
        click.echo("❌ Firmware installation failed!")
        sys.exit(1)

@cli.command()
@click.pass_context
def health(ctx):
    """Run comprehensive health checks"""
    click.echo("🔍 Running comprehensive health checks...")
    
    cli_integration = CLIIntegration(ctx.obj['config'])
    health_checks = cli_integration.automation.run_comprehensive_health_check()
    
    click.echo("\n" + cli_integration.format_health_check_table(health_checks))
    
    critical_count = sum(1 for check in health_checks if check.status == HealthStatus.CRITICAL)
    warning_count = sum(1 for check in health_checks if check.status == HealthStatus.WARNING)
    healthy_count = sum(1 for check in health_checks if check.status == HealthStatus.HEALTHY)
    
    click.echo(f"\n📊 Summary: {healthy_count} healthy, {warning_count} warnings, {critical_count} critical")
    
    if critical_count > 0:
        sys.exit(1)

@cli.command()
@click.argument('failure_type', type=click.Choice([ft.value for ft in FailureType]))
@click.pass_context
def recover(ctx, failure_type):
    """Execute recovery for specific failure scenario"""
    click.echo(f"🔧 Executing recovery for failure type: {failure_type}")
    
    automation = NICFirmwareAutomation(ctx.obj['config'])
    failure_enum = FailureType(failure_type)
    
    success = automation.handle_failure_scenario(failure_enum)
    
    if success:
        click.echo("✅ Recovery completed successfully!")
        sys.exit(0)
    else:
        click.echo("❌ Recovery failed!")
        sys.exit(1)

@cli.command()
@click.option('--output', '-o', help='Output file for debug data')
@click.pass_context
def debug(ctx, output):
    """Capture debug logs and generate techsupport"""
    click.echo("🐛 Capturing debug information...")
    
    automation = NICFirmwareAutomation(ctx.obj['config'])
    
    debug_data = automation.capture_debug_logs()
    click.echo(f"📝 Captured debug data for {len(debug_data)} commands")
    
    techsupport_path = automation.generate_techsupport()
    click.echo(f"📦 Generated techsupport bundle: {techsupport_path}")
    
    if output:
        with open(output, 'w') as f:
            json.dump(debug_data, f, indent=2)
        click.echo(f"💾 Debug data saved to: {output}")

@cli.command()
@click.pass_context
def scenarios(ctx):
    """List available failure scenarios and recovery recipes"""
    click.echo("📋 Available failure scenarios and recovery recipes:")
    
    cli_integration = CLIIntegration(ctx.obj['config'])
    click.echo("\n" + cli_integration.format_failure_scenarios_table())

@cli.command()
@click.argument('recipe_name')
@click.pass_context
def recipe(ctx, recipe_name):
    """Execute specific recovery recipe"""
    click.echo(f"🔧 Executing recovery recipe: {recipe_name}")
    
    automation = NICFirmwareAutomation(ctx.obj['config'])
    success = automation.execute_recovery_recipe(recipe_name)
    
    if success:
        click.echo("✅ Recovery recipe completed successfully!")
        sys.exit(0)
    else:
        click.echo("❌ Recovery recipe failed!")
        sys.exit(1)

@cli.command()
@click.pass_context
def status(ctx):
    """Show current system status and recent automation runs"""
    click.echo("📊 System Status Dashboard")
    click.echo("=" * 50)
    
    automation = NICFirmwareAutomation(ctx.obj['config'])
    
    click.echo("\n🔧 Configuration:")
    click.echo(f"  NIC Interface: {automation.config['nic_interface']}")
    click.echo(f"  Log Path: {automation.config['log_path']}")
    click.echo(f"  Debug Mode: {automation.config['debug_mode']}")
    
    log_path = automation.config['log_path']
    if os.path.exists(log_path):
        log_files = [f for f in os.listdir(log_path) if f.endswith('.log')]
        log_files.sort(reverse=True)
        
        click.echo(f"\n📝 Recent Log Files ({len(log_files)}):")
        for log_file in log_files[:5]:
            file_path = os.path.join(log_path, log_file)
            file_size = os.path.getsize(file_path)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            click.echo(f"  - {log_file} ({file_size} bytes, {file_time.strftime('%Y-%m-%d %H:%M:%S')})")
    
    click.echo("\n🔍 Quick Health Check:")
    health_checks = automation.run_comprehensive_health_check()
    
    for check in health_checks:
        status_icon = {
            HealthStatus.HEALTHY: "✅",
            HealthStatus.WARNING: "⚠️",
            HealthStatus.CRITICAL: "❌",
            HealthStatus.UNKNOWN: "❓"
        }.get(check.status, "❓")
        
        click.echo(f"  {status_icon} {check.name}: {check.message}")

@cli.command()
@click.pass_context
def test(ctx):
    """Run automation test suite"""
    click.echo("🧪 Running automation test suite...")
    
    try:
        from test_nic_automation import (
            test_successful_installation,
            test_failure_scenarios,
            test_health_checks,
            test_debug_logging,
            test_recovery_recipes
        )
        
        tests = [
            ("Health Checks", test_health_checks),
            ("Debug Logging", test_debug_logging),
            ("Recovery Recipes", test_recovery_recipes),
            ("Failure Scenarios", test_failure_scenarios),
            ("Successful Installation", test_successful_installation)
        ]
        
        results = {}
        for test_name, test_func in tests:
            click.echo(f"\n🔬 Running {test_name}...")
            try:
                result = test_func()
                results[test_name] = result
                status = "✅ PASSED" if result else "❌ FAILED"
                click.echo(f"   {status}")
            except Exception as e:
                results[test_name] = False
                click.echo(f"   ❌ FAILED: {e}")
        
        click.echo("\n📊 Test Summary:")
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        click.echo(f"   {passed}/{total} tests passed")
        
        if passed == total:
            click.echo("🎉 All tests passed!")
            sys.exit(0)
        else:
            click.echo("❌ Some tests failed!")
            sys.exit(1)
            
    except ImportError as e:
        click.echo(f"❌ Error importing test modules: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
