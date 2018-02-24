   #include "mpi.h"
   #include <sys/time.h>
   #include <stdio.h>

   double When()
{
    struct timeval tp;
    gettimeofday(&tp, NULL);
    return ((double) tp.tv_sec + (double) tp.tv_usec * 1e-6);
}

   void main(int argc, char *argv[])  {
   int dest, source, count, tag=1;  
   char inmsg, outmsg='h';
   MPI_Status Stat;   // required variable for receive routines

   int  numtasks, rank, len, rc;
   char hostname[MPI_MAX_PROCESSOR_NAME];

   // initialize MPI
   MPI_Init(&argc,&argv);

   // get number of tasks
   MPI_Comm_size(MPI_COMM_WORLD,&numtasks);

   // get my rank
   MPI_Comm_rank(MPI_COMM_WORLD,&rank);

   // this one is obvious
   MPI_Get_processor_name(hostname, &len);
   //printf ("Number of tasks= %d My rank= %d Running on %s\n", numtasks,rank,hostname);
   
   int init_tc_system = 0;
   int n = 5; 
while(n != 0)
{
   // task 0 sends to task 1 and waits to receive a return message
   if (rank%2 == 0) {
     dest = ((rank)+1)%numtasks;
     source = rank;
     //printf("sending process rank %d to rank %d\n",source,dest); 
     double time_start = When();
     MPI_Ssend(&outmsg, 1, MPI_CHAR, dest, tag, MPI_COMM_WORLD);
     //MPI_Recv(&inmsg, 1, MPI_CHAR, source, tag, MPI_COMM_WORLD, &Stat);
     double time_end = When();

     double rtt = time_end-time_start;  
     printf("rtt : %f\n",rtt); 
   } 

   // task 1 waits for task 0 message then returns a message
   else if (rank%2 != 0) {
     dest = rank;
     source = rank-1;
     //printf("waiting for reciv %d\n",rank);
     MPI_Recv(&inmsg, 1, MPI_CHAR, source, tag, MPI_COMM_WORLD, &Stat);
     //MPI_Send(&outmsg, 1, MPI_CHAR, dest, tag, MPI_COMM_WORLD);
     MPI_Get_count(&Stat, MPI_CHAR, &count);
     //printf("Task %d: Received %d char(s) from task %d to %d with tag %d Running on %s \n",
   //       rank, count, Stat.MPI_SOURCE, dest, Stat.MPI_TAG,hostname);
     //MPI_Send(&outmsg, 1, MPI_CHAR, Stat.MPI_SOURCE, tag, MPI_COMM_WORLD); 
    }
  /* if(!init_tc_system)
   {
      system("sudo python mpi_network_emu.py");
      init_tc_system = 1;
   }*/
   n--;
}
 
   MPI_Finalize();
   }
