#include <iostream>
#include "TRandom3.h"
#include "TMath.h"

struct CrystalBall{
    static const double pi;
    static const double SPiO2;
    static const double S2;

    double m;
    double s;
    double a;
    double n;

    double B;
    double C;
    double D;
    double N;

    double NA;
    double Ns;
    double NC;
    double F;
    double G;
    double k;

    double cdfMa;
    double cdfPa;

    CrystalBall(){
	init(0, 1, 10, 10);
    }
    CrystalBall(double m_, double s_, double a_, double n_){
	init(m_, s_, a_, n_);
    }

    void init(double m_, double s_, double a_, double n_){
	m=m_;
	s=s_;
	a=a_;
	n=n_;

	double fa   = fabs(a);
	double expa = exp(-fa*fa/2);
	double A    = pow(n/fa, n)*expa;
	double C1   = n/fa/(n-1)*expa;
	double D1   = 2*SPiO2*erf(fa/S2);

	B  = n/fa-fa;
	C  = (D1+2*C1)/C1;
	D  = (D1+2*C1)/2;

	N  = 1.0/s/(D1+2*C1);
	k  = 1.0/(n-1);

	NA = N*A;
	Ns = N*s;
	NC = Ns*C1;
	F  = 1-fa*fa/n;
	G  = s*n/fa;

	cdfMa=cdf(m-a*s);
	cdfPa=cdf(m+a*s);
    }

    double pdf(double x) const{
	double d=(x-m)/s;
	if(d<-a) return NA*pow(B-d, -n);
	if(d> a) return NA*pow(B+d, -n);
	return N*exp(-d*d/2);
    }

    double pdf(double x, double ks, double dm) const{
	double d=(x-m-dm)/(s*ks);
	if(d<-a) return NA/ks*pow(B-d, -n);
	if(d> a) return NA/ks*pow(B+d, -n);
	return N/ks*exp(-d*d/2);
    }

    double cdf(double x) const{
	double d = (x-m)/s;
	if(d<-a) return NC / pow(F-s*d/G, n-1);
	if(d> a) return NC * (C - pow(F+s*d/G, 1-n) );
	return Ns*(D-SPiO2*erf(-d/S2));
    }

    double invcdf(double u) const{
	if(u<cdfMa) return m + G*(F - pow(NC/u,    k) );
	if(u>cdfPa) return m - G*(F - pow(C-u/NC, -k) );
	return m - S2*s*TMath::ErfInverse((D - u/Ns ) / SPiO2);
    }
};
const double CrystalBall::pi    = TMath::Pi();
const double CrystalBall::SPiO2 = sqrt(TMath::Pi()/2.0);
const double CrystalBall::S2    = sqrt(2.0);


class RocRes{
    private:
	static const int NMAXETA=12;
	static const int NMAXTRK=12;

	int NETA;
	int NTRK;
	int NMIN;

	double BETA[NMAXETA+1];
	double ntrk[NMAXETA][NMAXTRK+1];
	double dtrk[NMAXETA][NMAXTRK+1];

	double width[NMAXETA][NMAXTRK];
	double alpha[NMAXETA][NMAXTRK];
	double power[NMAXETA][NMAXTRK];

	double rmsA[NMAXETA][NMAXTRK];
	double rmsB[NMAXETA][NMAXTRK];
	double rmsC[NMAXETA][NMAXTRK];

	double kDat[NMAXETA];
	double kRes[NMAXETA];

	int getBin(double x, const int NN, const double *b) const;


    public:
	enum TYPE {MC, Data, Extra};

	CrystalBall  cb[NMAXETA][NMAXTRK];

	RocRes();
	int getEtaBin(double feta) const;
	int getNBinDT(double v, int H) const;
	int getNBinMC(double v, int H) const;
	double getUrnd(int H, int F, double v) const;
	void dumpParams();
	void init(std::string filename);

	void reset();

	~RocRes(){}

	double Sigma(double pt, int H, int F) const;
	double kSpread(double gpt, double rpt, double eta, int nlayers, double w) const;
	double kSmear(double pt, double eta, TYPE type, double v, double u) const;
	double kSmear(double pt, double eta, TYPE type, double v, double u, int n) const;
	double kExtra(double pt, double eta, int nlayers, double u, double w) const;
	double getkDat(int H) const{return kDat[H];}
	double getkRes(int H) const{return kRes[H];}
};


class RocOne{
    private:
	static const int NMAXETA=22;
	static const int NMAXPHI=16;
	static const double MPHI;

	int NETA;
	int NPHI;

	double BETA[NMAXETA+1];
	double DPHI;

	double M[2][NMAXETA][NMAXPHI];
	double A[2][NMAXETA][NMAXPHI];
	double D[2][NMAXETA];

	RocRes RR;

	int getBin(double x, const int NN, const double *b) const;
	int getBin(double x, const int nmax, const double xmin, const double dx) const;

    public:
	enum TYPE{MC, DT};

	RocOne();
	~RocOne(){}

	RocOne(std::string filename, int iTYPE=0, int iSYS=0, int iMEM=0);
	bool checkSYS(int iSYS, int iMEM, int kSYS=0, int kMEM=0);
	bool checkTIGHT(int iTYPE, int iSYS, int iMEM, int kTYPE=0, int kSYS=0, int kMEM=0);
	void reset();
	void init(std::string filename, int iTYPE=0, int iSYS=0, int iMEM=0);

	double kScaleDT(int Q, double pt, double eta, double phi) const;
	double kScaleMC(int Q, double pt, double eta, double phi, double kSMR=1) const;
	double kScaleAndSmearMC(int Q, double pt, double eta, double phi, int n, double u, double w) const;
	double kScaleFromGenMC(int Q, double pt, double eta, double phi, int n, double gt, double w) const;
	double kGenSmear(double pt, double eta, double v, double u, RocRes::TYPE TT=RocRes::Data) const;

	double getM(int T, int H, int F) const{return M[T][H][F];}
	double getA(int T, int H, int F) const{return A[T][H][F];}
	double getK(int T, int H) const{return T==DT?RR.getkDat(H):RR.getkRes(H);}
	RocRes& getR() {return RR;}
};


class RoccoR{
    public:
	RoccoR();
	RoccoR(std::string dirname);
	~RoccoR();

	void init(std::string dirname);

	double kGenSmear(double pt, double eta, double v, double u, RocRes::TYPE TT=RocRes::Data, int s=0, int m=0) const;
	double kScaleDT(int Q, double pt, double eta, double phi, int s=0, int m=0) const;

	double kScaleAndSmearMC(int Q, double pt, double eta, double phi, int n, double u, double w, int s=0, int m=0) const;
	double kScaleFromGenMC(int Q, double pt, double eta, double phi, int n, double gt, double w, int s=0, int m=0) const;


	double getM(int T, int H, int F, int E=0, int m=0) const{return RC[E][m].getM(T,H,F);}
	double getA(int T, int H, int F, int E=0, int m=0) const{return RC[E][m].getA(T,H,F);}
	double getK(int T, int H, int E=0, int m=0)        const{return RC[E][m].getK(T,H);}

	int Nset() const{return RC.size();}
	int Nmem(int s=0) const{return RC[s].size();}

    private:
	std::vector<std::vector<RocOne> > RC;
};
