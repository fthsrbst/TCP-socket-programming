
#TCP soket kütüphanesi import ediyoruz
import socket
import sys
import select
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

# Başlık
console.clear()
console.print()
console.print("[bold red]" + "─" * 70 + "[/bold red]")
console.print()

ascii_title = """
[bold red]███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║[/bold red]
"""
console.print(ascii_title)
console.print("[dim]TCP Socket Server - Real-time Communication Tool[/dim]")
console.print()
console.print("[bold red]" + "─" * 70 + "[/bold red]")
console.print()

#socket değişkeni yaratılıyor
s = socket.socket()
# SO_REUSEADDR: Portu hemen yeniden kullanabilmemizi sağlar
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
console.print("  [green]●[/green] Socket oluşturuldu")

#dinlenecek port numarası 9998 olarak belirliyoruz.
port = 9998

#soketi yerel IP ve Porta bağla. '' parametresi tüm ağ arayüzlerini temsil eder (0.0.0.0)
s.bind(('',port))
console.print(f"  [green]●[/green] Port bağlandı: [cyan]{port}[/cyan]")

#dinleme modu
s.listen(5) #buradaki 5 backlog yani bağlantı kuyruğunun maksimum uzunluğu
console.print("  [yellow]●[/yellow] Dinleme modunda...")
console.print()

# Bağlantı bekleniyor paneli
waiting_panel = Panel(
    "[yellow]Client bağlantısı bekleniyor...[/yellow]",
    title="[bold]Durum[/bold]",
    border_style="yellow",
    box=box.ROUNDED
)
console.print(waiting_panel)

try:
    c, addr = s.accept()
    console.print()
    
    # Bağlantı bilgisi paneli
    connection_panel = Panel(
        f"[green]✓ Bağlantı başarılı[/green]\n[dim]IP:[/dim] [cyan]{addr[0]}[/cyan]\n[dim]Port:[/dim] [cyan]{addr[1]}[/cyan]",
        title="[bold]Bağlantı[/bold]",
        border_style="green",
        box=box.ROUNDED
    )
    console.print(connection_panel)
    
    c.send("Bağlandığınız için teşekkürler".encode())
    
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

    inputs = [c, sys.stdin]  # soket + klavye
    console.print("[bold magenta]Server:[/bold magenta] ", end="")
    
    while True:
        readable, _, _ = select.select(inputs, [], [])
        for r in readable:
            if r is c:
                data = c.recv(4096)
                if not data:
                    console.print("\n[red]✗ Client bağlantısı kesildi.[/red]")
                    raise SystemExit
                msg = data.decode().rstrip("\n")
                # Alınan mesaj, mevcut promptu bozmadan yazılsın
                console.print(f"\r[bold green]Client:[/bold green] {msg}")
                console.print("[bold magenta]Server:[/bold magenta] ", end="")
                if msg.strip().lower() == "quit":
                    console.print("\n[yellow]Client sohbeti sonlandırdı.[/yellow]")
                    raise SystemExit
            else:  # sys.stdin
                line = sys.stdin.readline()
                if not line:
                    continue
                msg = line.rstrip("\n")
                if msg.strip():  # Boş mesaj gönderme
                    c.send((msg + "\n").encode())
                    if msg.strip().lower() == "quit":
                        console.print("\n[yellow]Sohbet sonlandırıldı.[/yellow]")
                        raise SystemExit
                # tekrar prompt göster
                console.print("[bold magenta]Server:[/bold magenta] ", end="")



except KeyboardInterrupt:
    console.print("\n[red]⚠ Server kesildi, kapatılıyor.[/red]")
finally:
    c.close()
    s.close()
