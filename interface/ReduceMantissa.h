#ifndef reducemantissa_h
#define reducemantissa_h

class ReduceMantissaToNbitsRounding {
            public:
                ReduceMantissaToNbitsRounding(int bits) : 
                    shift(23-bits), mask((0xFFFFFFFF >> (shift)) << (shift)), 
                    test(1 << (shift-1)), maxn((1<<bits)-2) {
                        assert(bits <= 23); // "max mantissa size is 23 bits"
                    }
                float operator()(float f) const {
                    constexpr uint32_t low23 = (0x007FFFFF); // mask to keep lowest 23 bits = mantissa
                    constexpr uint32_t  hi9  = (0xFF800000); // mask to keep highest 9 bits = the rest
                    union { float flt; uint32_t i32; } conv;
                    conv.flt=f;
                    if (conv.i32 & test) { // need to round
                        uint32_t mantissa = (conv.i32 & low23) >> shift;
                        if (mantissa < maxn) mantissa++;
                        conv.i32 = (conv.i32 & hi9) | (mantissa << shift);
                    } else {
                        conv.i32 &= mask;
                    }
                    return conv.flt;
                }
            private:
                const int shift;
                const uint32_t mask, test, maxn;           
};


#endif
