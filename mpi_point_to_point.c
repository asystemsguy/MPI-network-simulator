   #include "mpi.h"
   #include <stdio.h>

   main(int argc, char *argv[])  {
   int dest, source, count, tag=1;  
   char inmsg, outmsg='h';
   MPI_Status Stat;   // required variable for receive routines

   //MPI_Init(&argc,&argv);
   //MPI_Comm_size(MPI_COMM_WORLD, &numtasks);
   //MPI_Comm_rank(MPI_COMM_WORLD, &rank);
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
   printf ("Number of tasks= %d My rank= %d Running on %s\n", numtasks,rank,hostname);

   // task 0 sends to task 1 and waits to receive a return message
   if (rank%2 == 0) {
     dest = ((rank)+1)%numtasks;
     source = rank;
     printf("sending process rank %d to rank %d\n",source,dest); 
     MPI_Send(&outmsg, 1, MPI_CHAR, dest, tag, MPI_COMM_WORLD);
     MPI_Recv(&inmsg, 1, MPI_CHAR, source, tag, MPI_COMM_WORLD, &Stat);
     } 

   // task 1 waits for task 0 message then returns a message
   else {
     dest = rank;
     source = rank-1;
     printf("waiting for reciv %d\n",rank);
     MPI_Recv(&inmsg, 1, MPI_CHAR, source, tag, MPI_COMM_WORLD, &Stat);
     //MPI_Send(&outmsg, 1, MPI_CHAR, dest, tag, MPI_COMM_WORLD);
     MPI_Get_count(&Stat, MPI_CHAR, &count);
   printf("Task %d: Received %d char(s) from task %d with tag %d Running on %s \n",
          rank, count, Stat.MPI_SOURCE, Stat.MPI_TAG,hostname); 
    }

   // query recieve Stat variable and print message details
  // MPI_Get_count(&Stat, MPI_CHAR, &count);
  // printf("Task %d: Received %d char(s) from task %d with tag %d Running on %s \n",
   //       rank, count, Stat.MPI_SOURCE, Stat.MPI_TAG,hostname);

   MPI_Finalize();
   }
