using CP;
{string} Flows = ...;
{string} Jobs = ...;
// Generate this in Scala, but not dependent on actual data
int AllowedFlows[Flows][Flows] = ...;
// change to m -> read from data
int numConstraints = ...;                 
range Constraints = 1 .. numConstraints;

int A[Constraints][Flows] = ... ;           
int C[Constraints] = ...;
int JobId = ...; // ID for saving file

dvar int+ B[Flows]; //flattened
dvar boolean I[Flows][Jobs];
dvar boolean Iflat[Flows];
dvar int BI[Flows];
dvar int BIjobs[Jobs];

minimize
  // 7c
  // No incentive to minimize any other values other than max tj
  max(j in Jobs)
    1 / BIjobs[j];
    
subject to {

  // 7d
  forall(c in Constraints)
    ct:
    sum(f in Flows)
      A[c][f] * BI[f] <= C[c];
      
  forall(f in Flows)
      Iflat[f]==sum (j in Jobs) I[f][j];
      
  forall(f in Flows)
    (Iflat[f]==1) => (BI[f]==B[f]);
  forall(f in Flows)
    (Iflat[f]==0) => (BI[f]==0);
  
  // 7b
  forall(j in Jobs)
    sum (f in Flows) I[f][j] == 1;
    
  
  forall(f in Flows)
    forall(j in Jobs)
      (I[f][j]==1) => (BIjobs[j]==BI[f]);
      
  forall(f in Flows)
      forall(f2 in Flows)
        ctFlows:
        Iflat[f] * Iflat[f2] <= AllowedFlows[f][f2];
}

execute DISPLAY {
  var f=new IloOplOutputFile(JobId + "_layer1_output.txt");
  f.writeln("I");
  f.writeln(I);
};
