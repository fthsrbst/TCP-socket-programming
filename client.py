import socket
import select
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

# Başlık
console.clear()
console.print()
console.print("[bold cyan]" + "─" * 70 + "[/bold cyan]")
console.print()

ascii_title = """
[bold cyan] ██████╗██╗     ██╗███████╗███╗   ██╗████████╗
██╔════╝██║     ██║██╔════╝████╗  ██║╚══██╔══╝
██║     ██║     ██║█████╗  ██╔██╗ ██║   ██║   
██║     ██║     ██║██╔══╝  ██║╚██╗██║   ██║   
╚██████╗███████╗██║███████╗██║ ╚████║   ██║   [/bold cyan]
"""
console.print(ascii_title)
console.print("[dim]TCP Socket Client - Real-time Communication Tool[/dim]")
console.print()
console.print("[bold cyan]" + "─" * 70 + "[/bold cyan]")
console.print()

s=socket.socket()
console.print("  [green]●[/green] Socket başlatıldı")

port=9998
s.connect(('127.0.0.1',port))
console.print(f"  [green]●[/green] Server'a bağlanıldı: [cyan]127.0.0.1:{port}[/cyan]")

# Bilgi paneli
info_panel = Panel(
    "[yellow]• Mesaj göndermek için yazıp Enter'a basın\n• Çıkmak için 'quit' yazın[/yellow]",
    title="[bold]Bilgi[/bold]",
    border_style="blue",
    box=box.ROUNDED
)
console.print(info_panel)
console.print("─" * 50)
console.print()

try:
    inputs = [s, sys.stdin]
    console.print("[bold green]Client:[/bold green] ", end="")
    while True:
        readable, _, _ = select.select(inputs, [], [])
        for r in readable:
            if r is s:
                data = s.recv(4096)
                if not data:
                    console.print("\n[red]✗ Server bağlantısı kesildi.[/red]")
                    raise SystemExit
                msg = data.decode().rstrip("\n")
                console.print(f"\r[bold blue]Server:[/bold blue] {msg}")
                console.print("[bold green]Client:[/bold green] ", end="")
                if msg.strip().lower() == "quit":
                    console.print("\n[yellow]Server sohbeti sonlandırdı.[/yellow]")
                    raise SystemExit
            else:  # sys.stdin
                line = sys.stdin.readline()
                if not line:
                    continue
                msg = line.rstrip("\n")
                if msg.strip():  # Boş mesaj gönderme
                    s.send((msg + "\n").encode())
                    if msg.strip().lower() == "quit":
                        console.print("\n[yellow]Sohbet sonlandırıldı.[/yellow]")
                        raise SystemExit
                console.print("[bold green]Client:[/bold green] ", end="")

finally:
    s.close()