/* census2.c — the periodic table of two-kind 1-D cross-amendment constitutions.
 *
 * Box (exactly specified):
 *   kinds        : 2
 *   rules        : all (a,b,c) in {-1,0,1}^3  (27 each -> 729 ordered pairs)
 *   target maps  : all 4 functions {0,1}->{0,1}:  id, swap, const0, const1
 *   constitutions: 729 * 4 = 2916
 *   seeds        : every code with support span <= SPANMAX, translation-
 *                  normalised (leftmost occupied cell = 0, rightmost occupied)
 *                  -> 3, 9, 36, 144, 576, 2304 for spans 1..6  = 3072
 *   window       : WBITS cells, seed based at BASE, escape margin MARGIN
 *   budget       : MAXT steps
 *   modes        : parity and OR
 *
 * Classification (same certificates as xnomos.classify):
 *   EXTINCT, FIXED, BALANCED (fixed with >=1 active law), CYCLE-p,
 *   GLIDER (normalised recurrence with nonzero displacement), GROWING
 *   (escaped the window), UNRESOLVED (budget exhausted).
 *
 * Build: clang -O2 -o census2 census2.c
 * Run  : ./census2 <spanmax> <mode 0=parity 1=or> > out.csv
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define NW      5                     /* 3 * 64 = 192 cells */
#define WBITS   (NW*64)
#define MARGIN  28
#define BASE    150
#define MAXT    1024
#define HSZ     2048                  /* hash table slots (power of two) */

typedef struct { uint64_t w[NW]; } BB;

static inline void bb_zero(BB *x){ for(int i=0;i<NW;i++) x->w[i]=0; }
static inline int  bb_zerop(const BB*x){ for(int i=0;i<NW;i++) if(x->w[i]) return 0; return 1; }
static inline BB   bb_or (BB a, BB b){ BB r; for(int i=0;i<NW;i++) r.w[i]=a.w[i]|b.w[i]; return r; }
static inline BB   bb_and(BB a, BB b){ BB r; for(int i=0;i<NW;i++) r.w[i]=a.w[i]&b.w[i]; return r; }
static inline BB   bb_xor(BB a, BB b){ BB r; for(int i=0;i<NW;i++) r.w[i]=a.w[i]^b.w[i]; return r; }
static inline BB   bb_andn(BB a, BB b){ BB r; for(int i=0;i<NW;i++) r.w[i]=a.w[i]&~b.w[i]; return r; }
static inline int  bb_eq(const BB*a,const BB*b){ for(int i=0;i<NW;i++) if(a->w[i]!=b->w[i]) return 0; return 1; }

/* shift so that bit i of the result = bit (i+1) of the argument  ("occ>>1") */
static inline BB bb_dn(BB a){ BB r; for(int i=0;i<NW;i++){ r.w[i]=(a.w[i]>>1); if(i+1<NW) r.w[i]|=(a.w[i+1]<<63);} return r; }
/* shift so that bit i of the result = bit (i-1) of the argument  ("occ<<1") */
static inline BB bb_up(BB a){ BB r; for(int i=NW-1;i>=0;i--){ r.w[i]=(a.w[i]<<1); if(i-1>=0) r.w[i]|=(a.w[i-1]>>63);} return r; }
/* bit i of result = bit (i+d) of a, d in {-1,0,1} */
static inline BB bb_rd(BB a,int d){ return d==0?a:(d==1?bb_dn(a):bb_up(a)); }
/* bit (i+d) of result = bit i of a, d in {-1,0,1} */
static inline BB bb_wr(BB a,int d){ return d==0?a:(d==1?bb_up(a):bb_dn(a)); }

static inline int bb_low(const BB*x){          /* lowest set bit index, -1 if empty */
    for(int i=0;i<NW;i++) if(x->w[i]) return i*64+__builtin_ctzll(x->w[i]);
    return -1;
}
static inline int bb_high(const BB*x){
    for(int i=NW-1;i>=0;i--) if(x->w[i]) return i*64+63-__builtin_clzll(x->w[i]);
    return -1;
}
static inline int bb_pop(const BB*x){ int s=0; for(int i=0;i<NW;i++) s+=__builtin_popcountll(x->w[i]); return s; }

/* shift a bitboard down by n cells (n>=0) */
static BB bb_shift_dn(BB a,int n){
    BB r; bb_zero(&r);
    int wq=n>>6, bq=n&63;
    for(int i=0;i<NW;i++){
        int j=i+wq; if(j>=NW) break;
        uint64_t v=a.w[j]>>bq;
        if(bq && j+1<NW) v |= a.w[j+1]<<(64-bq);
        r.w[i]=v;
    }
    return r;
}

typedef struct { int a,b,c; } Rule;
typedef struct { Rule r[2]; int t[2]; } Cons;

typedef struct { BB p[2]; } St;

/* one synchronous step; or_mode: OR resolution instead of parity */
static inline St stepf(St s, const Cons*C, int or_mode){
    BB occ = bb_or(s.p[0], s.p[1]);
    BB tog[2]; bb_zero(&tog[0]); bb_zero(&tog[1]);
    for(int k=0;k<2;k++){
        /* act = p[k] & occ(i+a) & ~occ(i+b) */
        BB ga = bb_rd(occ, C->r[k].a);
        BB gb = bb_rd(occ, C->r[k].b);
        BB act = bb_andn(bb_and(s.p[k], ga), gb);
        if(bb_zerop(&act)) continue;
        BB em = bb_wr(act, C->r[k].c);
        int t = C->t[k];
        if(or_mode) tog[t]=bb_or(tog[t],em);
        else        tog[t]=bb_xor(tog[t],em);
    }
    St o; o.p[0]=bb_xor(s.p[0],tog[0]); o.p[1]=bb_xor(s.p[1],tog[1]);
    return o;
}

static inline int nactive(St s, const Cons*C){
    BB occ = bb_or(s.p[0], s.p[1]);
    int n=0;
    for(int k=0;k<2;k++){
        BB ga = bb_rd(occ, C->r[k].a), gb = bb_rd(occ, C->r[k].b);
        BB act = bb_andn(bb_and(s.p[k], ga), gb);
        n += bb_pop(&act);
    }
    return n;
}

enum { EXTINCT=0, FIXED, BALANCED, CYCLE, GLIDER, GROWING, UNRESOLVED, NCLS };
static const char*CLSN[NCLS]={"EXTINCT","FIXED","BALANCED","CYCLE","GLIDER","GROWING","UNRESOLVED"};

typedef struct { int cls, period, t0, disp, active, card; } Res;

static St     hist[MAXT+2];
static int    hanchor[MAXT+2];
static int32_t htab[HSZ];

static uint64_t hashst(const St*s){
    uint64_t h=1469598103934665603ULL;
    for(int k=0;k<2;k++) for(int i=0;i<NW;i++){ h^=s->p[k].w[i]; h*=1099511628211ULL; }
    return h;
}

static Res run(St s, const Cons*C, int or_mode){
    Res R; R.cls=UNRESOLVED; R.period=0; R.t0=0; R.disp=0; R.active=0; R.card=0;
    memset(htab,-1,sizeof(htab));
    for(int t=0;t<MAXT;t++){
        BB occ = bb_or(s.p[0], s.p[1]);
        if(bb_zerop(&occ)){ R.cls=EXTINCT; R.t0=t; return R; }
        int lo=bb_low(&occ), hi=bb_high(&occ);
        if(lo<MARGIN || hi>=WBITS-MARGIN){ R.cls=GROWING; R.t0=t; R.card=bb_pop(&occ); return R; }
        /* normalised state */
        St nm; nm.p[0]=bb_shift_dn(s.p[0],lo); nm.p[1]=bb_shift_dn(s.p[1],lo);
        uint64_t h=hashst(&nm);
        int slot=(int)(h&(HSZ-1));
        int hitat=-1;
        while(htab[slot]>=0){
            int u=htab[slot];
            if(bb_eq(&hist[u].p[0],&nm.p[0]) && bb_eq(&hist[u].p[1],&nm.p[1])){ hitat=u; break; }
            slot=(slot+1)&(HSZ-1);
        }
        if(hitat>=0){
            int d = lo - hanchor[hitat];
            int p = t - hitat;
            R.t0=hitat; R.period=p; R.disp=d; R.card=bb_pop(&occ);
            if(d!=0){ R.cls=GLIDER; return R; }
            if(p==1){ int na=nactive(s,C); R.active=na; R.cls = na? BALANCED : FIXED; return R; }
            R.cls=CYCLE; return R;
        }
        hist[t]=nm; hanchor[t]=lo; htab[slot]=t;
        s = stepf(s,C,or_mode);
    }
    return R;
}

/* ---- seed enumeration: all masks over `span` cells, ends nonempty ---- */
static int seedcount(int spanmax){
    int n=0;
    for(int s=1;s<=spanmax;s++){ int c=3; for(int i=0;i<s-2;i++) c*=4; if(s>=2) c*=3; n+= (s==1)?3:c; }
    return n;
}

/* validation mode: read seeds+constitutions from stdin, print verdicts */
static int validate(void){
    int a0,b0,c0,a1,b1,c1,t0,t1,mode,span,m[8];
    while(scanf("%d %d %d %d %d %d %d %d %d %d",&a0,&b0,&c0,&a1,&b1,&c1,&t0,&t1,&mode,&span)==10){
        for(int i=0;i<span;i++) scanf("%d",&m[i]);
        Cons C; C.r[0]=(Rule){a0,b0,c0}; C.r[1]=(Rule){a1,b1,c1}; C.t[0]=t0; C.t[1]=t1;
        St s; bb_zero(&s.p[0]); bb_zero(&s.p[1]);
        for(int i=0;i<span;i++){
            if(m[i]&1) s.p[0].w[(BASE+i)/64] |= 1ULL<<((BASE+i)&63);
            if(m[i]&2) s.p[1].w[(BASE+i)/64] |= 1ULL<<((BASE+i)&63);
        }
        Res R = run(s,&C,mode);
        printf("%s %d %d %d %d\n",CLSN[R.cls],R.period,R.t0,R.disp,R.active);
    }
    return 0;
}

int main(int argc,char**argv){
    if(argc>1 && !strcmp(argv[1],"-v")) return validate();
    int spanmax = argc>1?atoi(argv[1]):6;
    int or_mode = argc>2?atoi(argv[2]):0;

    Rule R27[27]; int nr=0;
    for(int a=-1;a<=1;a++)for(int b=-1;b<=1;b++)for(int c=-1;c<=1;c++){ R27[nr].a=a;R27[nr].b=b;R27[nr].c=c;nr++; }
    int TM[4][2]={{0,1},{1,0},{0,0},{1,1}};

    /* build the seed list once */
    int nseed=0, cap=1<<16;
    int (*seeds)[8] = malloc(sizeof(int)*8*cap);
    int *seedspan = malloc(sizeof(int)*cap);
    for(int s=1;s<=spanmax;s++){
        int mid=1; for(int i=0;i<s-2;i++) mid*=4;
        if(s==1){
            for(int m=1;m<4;m++){ memset(seeds[nseed],0,sizeof(int)*8); seeds[nseed][0]=m; seedspan[nseed]=1; nseed++; }
            continue;
        }
        for(int f=1;f<4;f++) for(int mi=0;mi<mid;mi++) for(int l=1;l<4;l++){
            memset(seeds[nseed],0,sizeof(int)*8);
            seeds[nseed][0]=f; seeds[nseed][s-1]=l;
            int q=mi; for(int i=0;i<s-2;i++){ seeds[nseed][i+1]=q&3; q>>=2; }
            seedspan[nseed]=s; nseed++;
        }
    }
    fprintf(stderr,"seeds=%d (predicted %d)\n",nseed,seedcount(spanmax));

    printf("r0a,r0b,r0c,r1a,r1b,r1c,t0,t1,extinct,fixed,balanced,cycle,glider,growing,unresolved,maxperiod,periodmask,maxtransient,nonpow2,maxactive,balanced0,cycle0\n");

    for(int i0=0;i0<27;i0++) for(int i1=0;i1<27;i1++) for(int tm=0;tm<4;tm++){
        Cons C; C.r[0]=R27[i0]; C.r[1]=R27[i1]; C.t[0]=TM[tm][0]; C.t[1]=TM[tm][1];
        long cnt[NCLS]; for(int i=0;i<NCLS;i++) cnt[i]=0;
        int maxp=0, maxtr=0, nonpow2=0, maxact=0; long bal0=0, cyc0=0;
        uint64_t pmask=0;
        for(int si=0;si<nseed;si++){
            St s; bb_zero(&s.p[0]); bb_zero(&s.p[1]);
            for(int i=0;i<seedspan[si];i++){
                int m=seeds[si][i];
                if(m&1) s.p[0].w[(BASE+i)/64] |= 1ULL<<((BASE+i)&63);
                if(m&2) s.p[1].w[(BASE+i)/64] |= 1ULL<<((BASE+i)&63);
            }
            Res R = run(s,&C,or_mode);
            cnt[R.cls]++;
            if(R.cls==CYCLE||R.cls==GLIDER){
                if(R.period>maxp) maxp=R.period;
                if(R.period<64) pmask |= 1ULL<<R.period;
                if(R.period&(R.period-1)) nonpow2++;
            }
            if(R.cls!=GROWING&&R.cls!=UNRESOLVED&&R.t0>maxtr) maxtr=R.t0;
            if(R.cls==BALANCED&&R.active>maxact) maxact=R.active;
            if(R.cls==BALANCED&&R.t0==0) bal0++;
            if(R.cls==CYCLE&&R.t0==0) cyc0++;
        }
        printf("%d,%d,%d,%d,%d,%d,%d,%d,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%d,%llu,%d,%d,%d,%ld,%ld\n",
            C.r[0].a,C.r[0].b,C.r[0].c,C.r[1].a,C.r[1].b,C.r[1].c,C.t[0],C.t[1],
            cnt[EXTINCT],cnt[FIXED],cnt[BALANCED],cnt[CYCLE],cnt[GLIDER],cnt[GROWING],cnt[UNRESOLVED],
            maxp,(unsigned long long)pmask,maxtr,nonpow2,maxact,bal0,cyc0);
    }
    return 0;
}
