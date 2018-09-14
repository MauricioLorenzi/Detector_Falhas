using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace DetectorFalhas
{
    class Program
    {
        static List<Processo> all_proc;

        static List<Processo> alive;

        static List<Processo> detected;

        static void Main(string[] args)
        {
            Processo p = new Processo();
            Processo p2 = new Processo();
            Processo p3 = new Processo();
            Processo p4 = new Processo();
            Processo p5 = new Processo();
            Processo p6 = new Processo();
            Processo p7 = new Processo();
            Processo p8 = new Processo();

            p.IP = "172.18.1.51";
            p.Name = "Aha";

            p2.IP = "172.18.1.71";
            p2.Name = "Aha";

            p3.IP = "172.18.1.69";
            p3.Name = "Aha";

            p4.IP = "172.17.143.127";
            p4.Name = "Aha";

            p5.IP = "172.17.97.212";
            p5.Name = "Aha";

            p6.IP = "172.18.1.64";
            p6.Name = "Aha";

            p7.IP = "172.18.3.8";
            p7.Name = "Aha";

            p8.IP = "172.18.1.43";
            p8.Name = "Aha";

            alive.Add(p);
            alive.Add(p2);
            alive.Add(p3);
            alive.Add(p4);
            alive.Add(p5);
            alive.Add(p6);
            alive.Add(p7);
            alive.Add(p8);

            all_proc.Add(p);
            all_proc.Add(p2);
            all_proc.Add(p3);
            all_proc.Add(p4);
            all_proc.Add(p5);
            all_proc.Add(p6);
            all_proc.Add(p7);
            all_proc.Add(p8);

            foreach (Processo proc in alive)
            {
                if(!alive.Contains(proc) && !detected.Contains(proc))
                {
                    detected.Add(proc);
                    alive.Remove(proc);
                }
            }

            //SocketInformation si = new SocketInformation();

            //Socket s = new Socket(si);

            Program program = new Program();

            Thread thread_listener = new Thread(program.Listen);

            
        }

        public void Listen(object data)
        {
            UdpClient uc_listener = new UdpClient(6001);

            IPEndPoint groupEP = new IPEndPoint(IPAddress.Any, 6001);

            uc_listener.Receive(ref groupEP);
        }

        public void Send(object data)
        {            
            UdpClient uc_sender = new UdpClient(6000);

            uc_sender.
        }
    }
}
