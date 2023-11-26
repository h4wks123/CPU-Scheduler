# CS 3104 Algorithms

This project is in fulfillment of my CS 3104 coding assignments in relation to operating system algorithms. The aforementioned algorithms ranges from both CPU scheduling (preemptive or non-preemptive) and page replacement. Feel free to improve my codes if there are any errors found, Thank you!

# CPU Scheduling

CPU scheduling refers to the switching between processes that are being executed. It forms the basis of multiprogrammed systems. This switching ensures that CPU utilization is maximized so that the computer is more productive.

There are two main types of CPU scheduling, preemptive and non-preemptive. Preemptive scheduling is when a process transitions from a running state to a ready state or from a waiting state to a ready state. Non-preemptive scheduling is employed when a process terminates or transitions from running to waiting state.

The following algorithms used for this includes: FCFS(first come first serve), SJF (shortest job first), SRTF (shortest remaining time first), priority preemptive, priority non-preemptive, RR (round robin), MLQ (multilayer queue), MLFQ (multilayer feedback queue)

# Page Replacement

Page replacement is needed in the operating systems that use virtual memory using Demand Paging. As we know in Demand paging, only a set of pages of a process is loaded into the memory. This is done so that we can have more processes in the memory at the same time.

When a page that is residing in virtual memory is requested by a process for its execution, the Operating System needs to decide which page will be replaced by this requested page. This process is known as page replacement and is a vital component in virtual memory management.

The following algorithms used for this includes: FCFS (first come first serve), LRU (least recently used), LFU (least frequently used), optimal.

# Programming Toolkit

The IDE used for this project is visual studio code and the language behind its algorithms is Python.
