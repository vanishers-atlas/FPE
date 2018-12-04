#include "header.h"


// **** Fire function declaration **** //
static inline void butterfly_sharecoe(int i0, int i1, int *o0, int *o1, int W) {
asm ("ADDMULSRA1 %[A0], %[b0], %[w0], %[a0]\n\t"
     "SUBMULSRA1 %[B0], %[b0], %[w0], %[a0]\n\t"
     : [A0]"=&r"(*o0), [B0]"=&r"(*o1)
     : [b0]"r"(i1), [w0]"i"(W), [a0]"r"(i0)
      );
}

// **** Main function **** //
void FPE1PE0() {

  // **** Variable declaration **** //
	int T256_i0;
	int T256_i1;
	int T256_o0;
	int T256_o1;
	int T256_W;

	int T257_i0;
	int T257_i1;
	int T257_o0;
	int T257_o1;
	int T257_W;

	int T258_i0;
	int T258_i1;
	int T258_o0;
	int T258_o1;
	int T258_W;

	int T259_i0;
	int T259_i1;
	int T259_o0;
	int T259_o1;
	int T259_W;

	int T260_i0;
	int T260_i1;
	int T260_o0;
	int T260_o1;
	int T260_W;

	int T261_i0;
	int T261_i1;
	int T261_o0;
	int T261_o1;
	int T261_W;

	int T262_i0;
	int T262_i1;
	int T262_o0;
	int T262_o1;
	int T262_W;

	int T263_i0;
	int T263_i1;
	int T263_o0;
	int T263_o1;
	int T263_W;

	int T264_i0;
	int T264_i1;
	int T264_o0;
	int T264_o1;
	int T264_W;

	int T265_i0;
	int T265_i1;
	int T265_o0;
	int T265_o1;
	int T265_W;

	int T266_i0;
	int T266_i1;
	int T266_o0;
	int T266_o1;
	int T266_W;

	int T267_i0;
	int T267_i1;
	int T267_o0;
	int T267_o1;
	int T267_W;

	int T268_i0;
	int T268_i1;
	int T268_o0;
	int T268_o1;
	int T268_W;

	int T269_i0;
	int T269_i1;
	int T269_o0;
	int T269_o1;
	int T269_W;

	int T270_i0;
	int T270_i1;
	int T270_o0;
	int T270_o1;
	int T270_W;

	int T271_i0;
	int T271_i1;
	int T271_o0;
	int T271_o1;
	int T271_W;

	int T272_i0;
	int T272_i1;
	int T272_o0;
	int T272_o1;
	int T272_W;

	int T273_i0;
	int T273_i1;
	int T273_o0;
	int T273_o1;
	int T273_W;

	int T274_i0;
	int T274_i1;
	int T274_o0;
	int T274_o1;
	int T274_W;

	int T275_i0;
	int T275_i1;
	int T275_o0;
	int T275_o1;
	int T275_W;

	int T276_i0;
	int T276_i1;
	int T276_o0;
	int T276_o1;
	int T276_W;

	int T277_i0;
	int T277_i1;
	int T277_o0;
	int T277_o1;
	int T277_W;

	int T278_i0;
	int T278_i1;
	int T278_o0;
	int T278_o1;
	int T278_W;

	int T279_i0;
	int T279_i1;
	int T279_o0;
	int T279_o1;
	int T279_W;

	int T280_i0;
	int T280_i1;
	int T280_o0;
	int T280_o1;
	int T280_W;

	int T281_i0;
	int T281_i1;
	int T281_o0;
	int T281_o1;
	int T281_W;

	int T282_i0;
	int T282_i1;
	int T282_o0;
	int T282_o1;
	int T282_W;

	int T283_i0;
	int T283_i1;
	int T283_o0;
	int T283_o1;
	int T283_W;

	int T284_i0;
	int T284_i1;
	int T284_o0;
	int T284_o1;
	int T284_W;

	int T285_i0;
	int T285_i1;
	int T285_o0;
	int T285_o1;
	int T285_W;

	int T286_i0;
	int T286_i1;
	int T286_o0;
	int T286_o1;
	int T286_W;

	int T287_i0;
	int T287_i1;
	int T287_o0;
	int T287_o1;
	int T287_W;

	int T288_i0;
	int T288_i1;
	int T288_o0;
	int T288_o1;
	int T288_W;

	int T289_i0;
	int T289_i1;
	int T289_o0;
	int T289_o1;
	int T289_W;

	int T290_i0;
	int T290_i1;
	int T290_o0;
	int T290_o1;
	int T290_W;

	int T291_i0;
	int T291_i1;
	int T291_o0;
	int T291_o1;
	int T291_W;

	int T292_i0;
	int T292_i1;
	int T292_o0;
	int T292_o1;
	int T292_W;

	int T293_i0;
	int T293_i1;
	int T293_o0;
	int T293_o1;
	int T293_W;

	int T294_i0;
	int T294_i1;
	int T294_o0;
	int T294_o1;
	int T294_W;

	int T295_i0;
	int T295_i1;
	int T295_o0;
	int T295_o1;
	int T295_W;

	int T296_i0;
	int T296_i1;
	int T296_o0;
	int T296_o1;
	int T296_W;

	int T297_i0;
	int T297_i1;
	int T297_o0;
	int T297_o1;
	int T297_W;

	int T298_i0;
	int T298_i1;
	int T298_o0;
	int T298_o1;
	int T298_W;

	int T299_i0;
	int T299_i1;
	int T299_o0;
	int T299_o1;
	int T299_W;

	int T300_i0;
	int T300_i1;
	int T300_o0;
	int T300_o1;
	int T300_W;

	int T301_i0;
	int T301_i1;
	int T301_o0;
	int T301_o1;
	int T301_W;

	int T302_i0;
	int T302_i1;
	int T302_o0;
	int T302_o1;
	int T302_W;

	int T303_i0;
	int T303_i1;
	int T303_o0;
	int T303_o1;
	int T303_W;

	int T304_i0;
	int T304_i1;
	int T304_o0;
	int T304_o1;
	int T304_W;

	int T305_i0;
	int T305_i1;
	int T305_o0;
	int T305_o1;
	int T305_W;

	int T306_i0;
	int T306_i1;
	int T306_o0;
	int T306_o1;
	int T306_W;

	int T307_i0;
	int T307_i1;
	int T307_o0;
	int T307_o1;
	int T307_W;

	int T308_i0;
	int T308_i1;
	int T308_o0;
	int T308_o1;
	int T308_W;

	int T309_i0;
	int T309_i1;
	int T309_o0;
	int T309_o1;
	int T309_W;

	int T310_i0;
	int T310_i1;
	int T310_o0;
	int T310_o1;
	int T310_W;

	int T311_i0;
	int T311_i1;
	int T311_o0;
	int T311_o1;
	int T311_W;

	int T312_i0;
	int T312_i1;
	int T312_o0;
	int T312_o1;
	int T312_W;

	int T313_i0;
	int T313_i1;
	int T313_o0;
	int T313_o1;
	int T313_W;

	int T314_i0;
	int T314_i1;
	int T314_o0;
	int T314_o1;
	int T314_W;

	int T315_i0;
	int T315_i1;
	int T315_o0;
	int T315_o1;
	int T315_W;

	int T316_i0;
	int T316_i1;
	int T316_o0;
	int T316_o1;
	int T316_W;

	int T317_i0;
	int T317_i1;
	int T317_o0;
	int T317_o1;
	int T317_W;

	int T318_i0;
	int T318_i1;
	int T318_o0;
	int T318_o1;
	int T318_W;

	int T319_i0;
	int T319_i1;
	int T319_o0;
	int T319_o1;
	int T319_W;

	int T320_i0;
	int T320_i1;
	int T320_o0;
	int T320_o1;
	int T320_W;

	int T321_i0;
	int T321_i1;
	int T321_o0;
	int T321_o1;
	int T321_W;

	int T322_i0;
	int T322_i1;
	int T322_o0;
	int T322_o1;
	int T322_W;

	int T323_i0;
	int T323_i1;
	int T323_o0;
	int T323_o1;
	int T323_W;

	int T324_i0;
	int T324_i1;
	int T324_o0;
	int T324_o1;
	int T324_W;

	int T325_i0;
	int T325_i1;
	int T325_o0;
	int T325_o1;
	int T325_W;

	int T326_i0;
	int T326_i1;
	int T326_o0;
	int T326_o1;
	int T326_W;

	int T327_i0;
	int T327_i1;
	int T327_o0;
	int T327_o1;
	int T327_W;

	int T328_i0;
	int T328_i1;
	int T328_o0;
	int T328_o1;
	int T328_W;

	int T329_i0;
	int T329_i1;
	int T329_o0;
	int T329_o1;
	int T329_W;

	int T330_i0;
	int T330_i1;
	int T330_o0;
	int T330_o1;
	int T330_W;

	int T331_i0;
	int T331_i1;
	int T331_o0;
	int T331_o1;
	int T331_W;

	int T332_i0;
	int T332_i1;
	int T332_o0;
	int T332_o1;
	int T332_W;

	int T333_i0;
	int T333_i1;
	int T333_o0;
	int T333_o1;
	int T333_W;

	int T334_i0;
	int T334_i1;
	int T334_o0;
	int T334_o1;
	int T334_W;

	int T335_i0;
	int T335_i1;
	int T335_o0;
	int T335_o1;
	int T335_W;

	int T336_i0;
	int T336_i1;
	int T336_o0;
	int T336_o1;
	int T336_W;

	int T337_i0;
	int T337_i1;
	int T337_o0;
	int T337_o1;
	int T337_W;

	int T338_i0;
	int T338_i1;
	int T338_o0;
	int T338_o1;
	int T338_W;

	int T339_i0;
	int T339_i1;
	int T339_o0;
	int T339_o1;
	int T339_W;

	int T340_i0;
	int T340_i1;
	int T340_o0;
	int T340_o1;
	int T340_W;

	int T341_i0;
	int T341_i1;
	int T341_o0;
	int T341_o1;
	int T341_W;

	int T342_i0;
	int T342_i1;
	int T342_o0;
	int T342_o1;
	int T342_W;

	int T343_i0;
	int T343_i1;
	int T343_o0;
	int T343_o1;
	int T343_W;

	int T344_i0;
	int T344_i1;
	int T344_o0;
	int T344_o1;
	int T344_W;

	int T345_i0;
	int T345_i1;
	int T345_o0;
	int T345_o1;
	int T345_W;

	int T346_i0;
	int T346_i1;
	int T346_o0;
	int T346_o1;
	int T346_W;

	int T347_i0;
	int T347_i1;
	int T347_o0;
	int T347_o1;
	int T347_W;

	int T348_i0;
	int T348_i1;
	int T348_o0;
	int T348_o1;
	int T348_W;

	int T349_i0;
	int T349_i1;
	int T349_o0;
	int T349_o1;
	int T349_W;

	int T350_i0;
	int T350_i1;
	int T350_o0;
	int T350_o1;
	int T350_W;

	int T351_i0;
	int T351_i1;
	int T351_o0;
	int T351_o1;
	int T351_W;

	int T352_i0;
	int T352_i1;
	int T352_o0;
	int T352_o1;
	int T352_W;

	int T353_i0;
	int T353_i1;
	int T353_o0;
	int T353_o1;
	int T353_W;

	int T354_i0;
	int T354_i1;
	int T354_o0;
	int T354_o1;
	int T354_W;

	int T355_i0;
	int T355_i1;
	int T355_o0;
	int T355_o1;
	int T355_W;

	int T356_i0;
	int T356_i1;
	int T356_o0;
	int T356_o1;
	int T356_W;

	int T357_i0;
	int T357_i1;
	int T357_o0;
	int T357_o1;
	int T357_W;

	int T358_i0;
	int T358_i1;
	int T358_o0;
	int T358_o1;
	int T358_W;

	int T359_i0;
	int T359_i1;
	int T359_o0;
	int T359_o1;
	int T359_W;

	int T360_i0;
	int T360_i1;
	int T360_o0;
	int T360_o1;
	int T360_W;

	int T361_i0;
	int T361_i1;
	int T361_o0;
	int T361_o1;
	int T361_W;

	int T362_i0;
	int T362_i1;
	int T362_o0;
	int T362_o1;
	int T362_W;

	int T363_i0;
	int T363_i1;
	int T363_o0;
	int T363_o1;
	int T363_W;

	int T364_i0;
	int T364_i1;
	int T364_o0;
	int T364_o1;
	int T364_W;

	int T365_i0;
	int T365_i1;
	int T365_o0;
	int T365_o1;
	int T365_W;

	int T366_i0;
	int T366_i1;
	int T366_o0;
	int T366_o1;
	int T366_W;

	int T367_i0;
	int T367_i1;
	int T367_o0;
	int T367_o1;
	int T367_W;

	int T368_i0;
	int T368_i1;
	int T368_o0;
	int T368_o1;
	int T368_W;

	int T369_i0;
	int T369_i1;
	int T369_o0;
	int T369_o1;
	int T369_W;

	int T370_i0;
	int T370_i1;
	int T370_o0;
	int T370_o1;
	int T370_W;

	int T371_i0;
	int T371_i1;
	int T371_o0;
	int T371_o1;
	int T371_W;

	int T372_i0;
	int T372_i1;
	int T372_o0;
	int T372_o1;
	int T372_W;

	int T373_i0;
	int T373_i1;
	int T373_o0;
	int T373_o1;
	int T373_W;

	int T374_i0;
	int T374_i1;
	int T374_o0;
	int T374_o1;
	int T374_W;

	int T375_i0;
	int T375_i1;
	int T375_o0;
	int T375_o1;
	int T375_W;

	int T376_i0;
	int T376_i1;
	int T376_o0;
	int T376_o1;
	int T376_W;

	int T377_i0;
	int T377_i1;
	int T377_o0;
	int T377_o1;
	int T377_W;

	int T378_i0;
	int T378_i1;
	int T378_o0;
	int T378_o1;
	int T378_W;

	int T379_i0;
	int T379_i1;
	int T379_o0;
	int T379_o1;
	int T379_W;

	int T380_i0;
	int T380_i1;
	int T380_o0;
	int T380_o1;
	int T380_W;

	int T381_i0;
	int T381_i1;
	int T381_o0;
	int T381_o1;
	int T381_W;

	int T382_i0;
	int T382_i1;
	int T382_o0;
	int T382_o1;
	int T382_W;

	int T383_i0;
	int T383_i1;
	int T383_o0;
	int T383_o1;
	int T383_W;

	int T384_i0;
	int T384_i1;
	int T384_o0;
	int T384_o1;
	int T384_W;

	int T385_i0;
	int T385_i1;
	int T385_o0;
	int T385_o1;
	int T385_W;

	int T386_i0;
	int T386_i1;
	int T386_o0;
	int T386_o1;
	int T386_W;

	int T387_i0;
	int T387_i1;
	int T387_o0;
	int T387_o1;
	int T387_W;

	int T388_i0;
	int T388_i1;
	int T388_o0;
	int T388_o1;
	int T388_W;

	int T389_i0;
	int T389_i1;
	int T389_o0;
	int T389_o1;
	int T389_W;

	int T390_i0;
	int T390_i1;
	int T390_o0;
	int T390_o1;
	int T390_W;

	int T391_i0;
	int T391_i1;
	int T391_o0;
	int T391_o1;
	int T391_W;

	int T392_i0;
	int T392_i1;
	int T392_o0;
	int T392_o1;
	int T392_W;

	int T393_i0;
	int T393_i1;
	int T393_o0;
	int T393_o1;
	int T393_W;

	int T394_i0;
	int T394_i1;
	int T394_o0;
	int T394_o1;
	int T394_W;

	int T395_i0;
	int T395_i1;
	int T395_o0;
	int T395_o1;
	int T395_W;

	int T396_i0;
	int T396_i1;
	int T396_o0;
	int T396_o1;
	int T396_W;

	int T397_i0;
	int T397_i1;
	int T397_o0;
	int T397_o1;
	int T397_W;

	int T398_i0;
	int T398_i1;
	int T398_o0;
	int T398_o1;
	int T398_W;

	int T399_i0;
	int T399_i1;
	int T399_o0;
	int T399_o1;
	int T399_W;

	int T400_i0;
	int T400_i1;
	int T400_o0;
	int T400_o1;
	int T400_W;

	int T401_i0;
	int T401_i1;
	int T401_o0;
	int T401_o1;
	int T401_W;

	int T402_i0;
	int T402_i1;
	int T402_o0;
	int T402_o1;
	int T402_W;

	int T403_i0;
	int T403_i1;
	int T403_o0;
	int T403_o1;
	int T403_W;

	int T404_i0;
	int T404_i1;
	int T404_o0;
	int T404_o1;
	int T404_W;

	int T405_i0;
	int T405_i1;
	int T405_o0;
	int T405_o1;
	int T405_W;

	int T406_i0;
	int T406_i1;
	int T406_o0;
	int T406_o1;
	int T406_W;

	int T407_i0;
	int T407_i1;
	int T407_o0;
	int T407_o1;
	int T407_W;

	int T408_i0;
	int T408_i1;
	int T408_o0;
	int T408_o1;
	int T408_W;

	int T409_i0;
	int T409_i1;
	int T409_o0;
	int T409_o1;
	int T409_W;

	int T410_i0;
	int T410_i1;
	int T410_o0;
	int T410_o1;
	int T410_W;

	int T411_i0;
	int T411_i1;
	int T411_o0;
	int T411_o1;
	int T411_W;

	int T412_i0;
	int T412_i1;
	int T412_o0;
	int T412_o1;
	int T412_W;

	int T413_i0;
	int T413_i1;
	int T413_o0;
	int T413_o1;
	int T413_W;

	int T414_i0;
	int T414_i1;
	int T414_o0;
	int T414_o1;
	int T414_W;

	int T415_i0;
	int T415_i1;
	int T415_o0;
	int T415_o1;
	int T415_W;

	int T416_i0;
	int T416_i1;
	int T416_o0;
	int T416_o1;
	int T416_W;

	int T417_i0;
	int T417_i1;
	int T417_o0;
	int T417_o1;
	int T417_W;

	int T418_i0;
	int T418_i1;
	int T418_o0;
	int T418_o1;
	int T418_W;

	int T419_i0;
	int T419_i1;
	int T419_o0;
	int T419_o1;
	int T419_W;

	int T420_i0;
	int T420_i1;
	int T420_o0;
	int T420_o1;
	int T420_W;

	int T421_i0;
	int T421_i1;
	int T421_o0;
	int T421_o1;
	int T421_W;

	int T422_i0;
	int T422_i1;
	int T422_o0;
	int T422_o1;
	int T422_W;

	int T423_i0;
	int T423_i1;
	int T423_o0;
	int T423_o1;
	int T423_W;

	int T424_i0;
	int T424_i1;
	int T424_o0;
	int T424_o1;
	int T424_W;

	int T425_i0;
	int T425_i1;
	int T425_o0;
	int T425_o1;
	int T425_W;

	int T426_i0;
	int T426_i1;
	int T426_o0;
	int T426_o1;
	int T426_W;

	int T427_i0;
	int T427_i1;
	int T427_o0;
	int T427_o1;
	int T427_W;

	int T428_i0;
	int T428_i1;
	int T428_o0;
	int T428_o1;
	int T428_W;

	int T429_i0;
	int T429_i1;
	int T429_o0;
	int T429_o1;
	int T429_W;

	int T430_i0;
	int T430_i1;
	int T430_o0;
	int T430_o1;
	int T430_W;

	int T431_i0;
	int T431_i1;
	int T431_o0;
	int T431_o1;
	int T431_W;

	int T432_i0;
	int T432_i1;
	int T432_o0;
	int T432_o1;
	int T432_W;

	int T433_i0;
	int T433_i1;
	int T433_o0;
	int T433_o1;
	int T433_W;

	int T434_i0;
	int T434_i1;
	int T434_o0;
	int T434_o1;
	int T434_W;

	int T435_i0;
	int T435_i1;
	int T435_o0;
	int T435_o1;
	int T435_W;

	int T436_i0;
	int T436_i1;
	int T436_o0;
	int T436_o1;
	int T436_W;

	int T437_i0;
	int T437_i1;
	int T437_o0;
	int T437_o1;
	int T437_W;

	int T438_i0;
	int T438_i1;
	int T438_o0;
	int T438_o1;
	int T438_W;

	int T439_i0;
	int T439_i1;
	int T439_o0;
	int T439_o1;
	int T439_W;

	int T440_i0;
	int T440_i1;
	int T440_o0;
	int T440_o1;
	int T440_W;

	int T441_i0;
	int T441_i1;
	int T441_o0;
	int T441_o1;
	int T441_W;

	int T442_i0;
	int T442_i1;
	int T442_o0;
	int T442_o1;
	int T442_W;

	int T443_i0;
	int T443_i1;
	int T443_o0;
	int T443_o1;
	int T443_W;

	int T444_i0;
	int T444_i1;
	int T444_o0;
	int T444_o1;
	int T444_W;

	int T445_i0;
	int T445_i1;
	int T445_o0;
	int T445_o1;
	int T445_W;

	int T446_i0;
	int T446_i1;
	int T446_o0;
	int T446_o1;
	int T446_W;

	int T447_i0;
	int T447_i1;
	int T447_o0;
	int T447_o1;
	int T447_W;

	int T448_i0;
	int T448_i1;
	int T448_o0;
	int T448_o1;
	int T448_W;

	int T449_i0;
	int T449_i1;
	int T449_o0;
	int T449_o1;
	int T449_W;

	int T450_i0;
	int T450_i1;
	int T450_o0;
	int T450_o1;
	int T450_W;

	int T451_i0;
	int T451_i1;
	int T451_o0;
	int T451_o1;
	int T451_W;

	int T452_i0;
	int T452_i1;
	int T452_o0;
	int T452_o1;
	int T452_W;

	int T453_i0;
	int T453_i1;
	int T453_o0;
	int T453_o1;
	int T453_W;

	int T454_i0;
	int T454_i1;
	int T454_o0;
	int T454_o1;
	int T454_W;

	int T455_i0;
	int T455_i1;
	int T455_o0;
	int T455_o1;
	int T455_W;

	int T456_i0;
	int T456_i1;
	int T456_o0;
	int T456_o1;
	int T456_W;

	int T457_i0;
	int T457_i1;
	int T457_o0;
	int T457_o1;
	int T457_W;

	int T458_i0;
	int T458_i1;
	int T458_o0;
	int T458_o1;
	int T458_W;

	int T459_i0;
	int T459_i1;
	int T459_o0;
	int T459_o1;
	int T459_W;

	int T460_i0;
	int T460_i1;
	int T460_o0;
	int T460_o1;
	int T460_W;

	int T461_i0;
	int T461_i1;
	int T461_o0;
	int T461_o1;
	int T461_W;

	int T462_i0;
	int T462_i1;
	int T462_o0;
	int T462_o1;
	int T462_W;

	int T463_i0;
	int T463_i1;
	int T463_o0;
	int T463_o1;
	int T463_W;

	int T464_i0;
	int T464_i1;
	int T464_o0;
	int T464_o1;
	int T464_W;

	int T465_i0;
	int T465_i1;
	int T465_o0;
	int T465_o1;
	int T465_W;

	int T466_i0;
	int T466_i1;
	int T466_o0;
	int T466_o1;
	int T466_W;

	int T467_i0;
	int T467_i1;
	int T467_o0;
	int T467_o1;
	int T467_W;

	int T468_i0;
	int T468_i1;
	int T468_o0;
	int T468_o1;
	int T468_W;

	int T469_i0;
	int T469_i1;
	int T469_o0;
	int T469_o1;
	int T469_W;

	int T470_i0;
	int T470_i1;
	int T470_o0;
	int T470_o1;
	int T470_W;

	int T471_i0;
	int T471_i1;
	int T471_o0;
	int T471_o1;
	int T471_W;

	int T472_i0;
	int T472_i1;
	int T472_o0;
	int T472_o1;
	int T472_W;

	int T473_i0;
	int T473_i1;
	int T473_o0;
	int T473_o1;
	int T473_W;

	int T474_i0;
	int T474_i1;
	int T474_o0;
	int T474_o1;
	int T474_W;

	int T475_i0;
	int T475_i1;
	int T475_o0;
	int T475_o1;
	int T475_W;

	int T476_i0;
	int T476_i1;
	int T476_o0;
	int T476_o1;
	int T476_W;

	int T477_i0;
	int T477_i1;
	int T477_o0;
	int T477_o1;
	int T477_W;

	int T478_i0;
	int T478_i1;
	int T478_o0;
	int T478_o1;
	int T478_W;

	int T479_i0;
	int T479_i1;
	int T479_o0;
	int T479_o1;
	int T479_W;

	int T480_i0;
	int T480_i1;
	int T480_o0;
	int T480_o1;
	int T480_W;

	int T481_i0;
	int T481_i1;
	int T481_o0;
	int T481_o1;
	int T481_W;

	int T482_i0;
	int T482_i1;
	int T482_o0;
	int T482_o1;
	int T482_W;

	int T483_i0;
	int T483_i1;
	int T483_o0;
	int T483_o1;
	int T483_W;

	int T484_i0;
	int T484_i1;
	int T484_o0;
	int T484_o1;
	int T484_W;

	int T485_i0;
	int T485_i1;
	int T485_o0;
	int T485_o1;
	int T485_W;

	int T486_i0;
	int T486_i1;
	int T486_o0;
	int T486_o1;
	int T486_W;

	int T487_i0;
	int T487_i1;
	int T487_o0;
	int T487_o1;
	int T487_W;

	int T488_i0;
	int T488_i1;
	int T488_o0;
	int T488_o1;
	int T488_W;

	int T489_i0;
	int T489_i1;
	int T489_o0;
	int T489_o1;
	int T489_W;

	int T490_i0;
	int T490_i1;
	int T490_o0;
	int T490_o1;
	int T490_W;

	int T491_i0;
	int T491_i1;
	int T491_o0;
	int T491_o1;
	int T491_W;

	int T492_i0;
	int T492_i1;
	int T492_o0;
	int T492_o1;
	int T492_W;

	int T493_i0;
	int T493_i1;
	int T493_o0;
	int T493_o1;
	int T493_W;

	int T494_i0;
	int T494_i1;
	int T494_o0;
	int T494_o1;
	int T494_W;

	int T495_i0;
	int T495_i1;
	int T495_o0;
	int T495_o1;
	int T495_W;

	int T496_i0;
	int T496_i1;
	int T496_o0;
	int T496_o1;
	int T496_W;

	int T497_i0;
	int T497_i1;
	int T497_o0;
	int T497_o1;
	int T497_W;

	int T498_i0;
	int T498_i1;
	int T498_o0;
	int T498_o1;
	int T498_W;

	int T499_i0;
	int T499_i1;
	int T499_o0;
	int T499_o1;
	int T499_W;

	int T500_i0;
	int T500_i1;
	int T500_o0;
	int T500_o1;
	int T500_W;

	int T501_i0;
	int T501_i1;
	int T501_o0;
	int T501_o1;
	int T501_W;

	int T502_i0;
	int T502_i1;
	int T502_o0;
	int T502_o1;
	int T502_W;

	int T503_i0;
	int T503_i1;
	int T503_o0;
	int T503_o1;
	int T503_W;

	int T504_i0;
	int T504_i1;
	int T504_o0;
	int T504_o1;
	int T504_W;

	int T505_i0;
	int T505_i1;
	int T505_o0;
	int T505_o1;
	int T505_W;

	int T506_i0;
	int T506_i1;
	int T506_o0;
	int T506_o1;
	int T506_W;

	int T507_i0;
	int T507_i1;
	int T507_o0;
	int T507_o1;
	int T507_W;

	int T508_i0;
	int T508_i1;
	int T508_o0;
	int T508_o1;
	int T508_W;

	int T509_i0;
	int T509_i1;
	int T509_o0;
	int T509_o1;
	int T509_W;

	int T510_i0;
	int T510_i1;
	int T510_o0;
	int T510_o1;
	int T510_W;

	int T511_i0;
	int T511_i1;
	int T511_o0;
	int T511_o1;
	int T511_W;


  // **** Parameter initialisation **** //
T256_W = 16384;
T257_W = -1073741824;
T258_W = 16384;
T259_W = -1073741824;
T260_W = 16384;
T261_W = -1073741824;
T262_W = 16384;
T263_W = -1073741824;
T264_W = 16384;
T265_W = -1073741824;
T266_W = 16384;
T267_W = -1073741824;
T268_W = 16384;
T269_W = -1073741824;
T270_W = 16384;
T271_W = -1073741824;
T272_W = 16384;
T273_W = -1073741824;
T274_W = 16384;
T275_W = -1073741824;
T276_W = 16384;
T277_W = -1073741824;
T278_W = 16384;
T279_W = -1073741824;
T280_W = 16384;
T281_W = -1073741824;
T282_W = 16384;
T283_W = -1073741824;
T284_W = 16384;
T285_W = -1073741824;
T286_W = 16384;
T287_W = -1073741824;
T288_W = 16384;
T289_W = -1073741824;
T290_W = 16384;
T291_W = -1073741824;
T292_W = 16384;
T293_W = -1073741824;
T294_W = 16384;
T295_W = -1073741824;
T296_W = 16384;
T297_W = -1073741824;
T298_W = 16384;
T299_W = -1073741824;
T300_W = 16384;
T301_W = -1073741824;
T302_W = 16384;
T303_W = -1073741824;
T304_W = 16384;
T305_W = -1073741824;
T306_W = 16384;
T307_W = -1073741824;
T308_W = 16384;
T309_W = -1073741824;
T310_W = 16384;
T311_W = -1073741824;
T312_W = 16384;
T313_W = -1073741824;
T314_W = 16384;
T315_W = -1073741824;
T316_W = 16384;
T317_W = -1073741824;
T318_W = 16384;
T319_W = -1073741824;
T320_W = 16384;
T321_W = -1073741824;
T322_W = 16384;
T323_W = -1073741824;
T324_W = 16384;
T325_W = -1073741824;
T326_W = 16384;
T327_W = -1073741824;
T328_W = 16384;
T329_W = -1073741824;
T330_W = 16384;
T331_W = -1073741824;
T332_W = 16384;
T333_W = -1073741824;
T334_W = 16384;
T335_W = -1073741824;
T336_W = 16384;
T337_W = -1073741824;
T338_W = 16384;
T339_W = -1073741824;
T340_W = 16384;
T341_W = -1073741824;
T342_W = 16384;
T343_W = -1073741824;
T344_W = 16384;
T345_W = -1073741824;
T346_W = 16384;
T347_W = -1073741824;
T348_W = 16384;
T349_W = -1073741824;
T350_W = 16384;
T351_W = -1073741824;
T352_W = 16384;
T353_W = -1073741824;
T354_W = 16384;
T355_W = -1073741824;
T356_W = 16384;
T357_W = -1073741824;
T358_W = 16384;
T359_W = -1073741824;
T360_W = 16384;
T361_W = -1073741824;
T362_W = 16384;
T363_W = -1073741824;
T364_W = 16384;
T365_W = -1073741824;
T366_W = 16384;
T367_W = -1073741824;
T368_W = 16384;
T369_W = -1073741824;
T370_W = 16384;
T371_W = -1073741824;
T372_W = 16384;
T373_W = -1073741824;
T374_W = 16384;
T375_W = -1073741824;
T376_W = 16384;
T377_W = -1073741824;
T378_W = 16384;
T379_W = -1073741824;
T380_W = 16384;
T381_W = -1073741824;
T382_W = 16384;
T383_W = -1073741824;
T384_W = 16384;
T385_W = -1073741824;
T386_W = 16384;
T387_W = -1073741824;
T388_W = 16384;
T389_W = -1073741824;
T390_W = 16384;
T391_W = -1073741824;
T392_W = 16384;
T393_W = -1073741824;
T394_W = 16384;
T395_W = -1073741824;
T396_W = 16384;
T397_W = -1073741824;
T398_W = 16384;
T399_W = -1073741824;
T400_W = 16384;
T401_W = -1073741824;
T402_W = 16384;
T403_W = -1073741824;
T404_W = 16384;
T405_W = -1073741824;
T406_W = 16384;
T407_W = -1073741824;
T408_W = 16384;
T409_W = -1073741824;
T410_W = 16384;
T411_W = -1073741824;
T412_W = 16384;
T413_W = -1073741824;
T414_W = 16384;
T415_W = -1073741824;
T416_W = 16384;
T417_W = -1073741824;
T418_W = 16384;
T419_W = -1073741824;
T420_W = 16384;
T421_W = -1073741824;
T422_W = 16384;
T423_W = -1073741824;
T424_W = 16384;
T425_W = -1073741824;
T426_W = 16384;
T427_W = -1073741824;
T428_W = 16384;
T429_W = -1073741824;
T430_W = 16384;
T431_W = -1073741824;
T432_W = 16384;
T433_W = -1073741824;
T434_W = 16384;
T435_W = -1073741824;
T436_W = 16384;
T437_W = -1073741824;
T438_W = 16384;
T439_W = -1073741824;
T440_W = 16384;
T441_W = -1073741824;
T442_W = 16384;
T443_W = -1073741824;
T444_W = 16384;
T445_W = -1073741824;
T446_W = 16384;
T447_W = -1073741824;
T448_W = 16384;
T449_W = -1073741824;
T450_W = 16384;
T451_W = -1073741824;
T452_W = 16384;
T453_W = -1073741824;
T454_W = 16384;
T455_W = -1073741824;
T456_W = 16384;
T457_W = -1073741824;
T458_W = 16384;
T459_W = -1073741824;
T460_W = 16384;
T461_W = -1073741824;
T462_W = 16384;
T463_W = -1073741824;
T464_W = 16384;
T465_W = -1073741824;
T466_W = 16384;
T467_W = -1073741824;
T468_W = 16384;
T469_W = -1073741824;
T470_W = 16384;
T471_W = -1073741824;
T472_W = 16384;
T473_W = -1073741824;
T474_W = 16384;
T475_W = -1073741824;
T476_W = 16384;
T477_W = -1073741824;
T478_W = 16384;
T479_W = -1073741824;
T480_W = 16384;
T481_W = -1073741824;
T482_W = 16384;
T483_W = -1073741824;
T484_W = 16384;
T485_W = -1073741824;
T486_W = 16384;
T487_W = -1073741824;
T488_W = 16384;
T489_W = -1073741824;
T490_W = 16384;
T491_W = -1073741824;
T492_W = 16384;
T493_W = -1073741824;
T494_W = 16384;
T495_W = -1073741824;
T496_W = 16384;
T497_W = -1073741824;
T498_W = 16384;
T499_W = -1073741824;
T500_W = 16384;
T501_W = -1073741824;
T502_W = 16384;
T503_W = -1073741824;
T504_W = 16384;
T505_W = -1073741824;
T506_W = 16384;
T507_W = -1073741824;
T508_W = 16384;
T509_W = -1073741824;
T510_W = 16384;
T511_W = -1073741824;

  // **** Code body **** //

	GET_FIFO(T256_i0, 0);
	GET_FIFO(T256_i1, 1);
	Butterfly(T256_i0, T256_i1, &T256_o0, &T256_o1, T256_W);
	PUT_FIFO(T256_o0, 0);
	PUT_FIFO(T256_o1, 1);

	GET_FIFO(T257_i0, 0);
	GET_FIFO(T257_i1, 1);
	Butterfly(T257_i0, T257_i1, &T257_o0, &T257_o1, T257_W);
	PUT_FIFO(T257_o0, 0);
	PUT_FIFO(T257_o1, 1);

	GET_FIFO(T258_i0, 0);
	GET_FIFO(T258_i1, 1);
	Butterfly(T258_i0, T258_i1, &T258_o0, &T258_o1, T258_W);
	PUT_FIFO(T258_o0, 2);
	PUT_FIFO(T258_o1, 3);

	GET_FIFO(T259_i0, 0);
	GET_FIFO(T259_i1, 1);
	Butterfly(T259_i0, T259_i1, &T259_o0, &T259_o1, T259_W);
	PUT_FIFO(T259_o0, 2);
	PUT_FIFO(T259_o1, 3);

	GET_FIFO(T260_i0, 0);
	GET_FIFO(T260_i1, 1);
	Butterfly(T260_i0, T260_i1, &T260_o0, &T260_o1, T260_W);
	PUT_FIFO(T260_o0, 0);
	PUT_FIFO(T260_o1, 1);

	GET_FIFO(T261_i0, 0);
	GET_FIFO(T261_i1, 1);
	Butterfly(T261_i0, T261_i1, &T261_o0, &T261_o1, T261_W);
	PUT_FIFO(T261_o0, 0);
	PUT_FIFO(T261_o1, 1);

	GET_FIFO(T262_i0, 0);
	GET_FIFO(T262_i1, 1);
	Butterfly(T262_i0, T262_i1, &T262_o0, &T262_o1, T262_W);
	PUT_FIFO(T262_o0, 2);
	PUT_FIFO(T262_o1, 3);

	GET_FIFO(T263_i0, 0);
	GET_FIFO(T263_i1, 1);
	Butterfly(T263_i0, T263_i1, &T263_o0, &T263_o1, T263_W);
	PUT_FIFO(T263_o0, 2);
	PUT_FIFO(T263_o1, 3);

	GET_FIFO(T264_i0, 0);
	GET_FIFO(T264_i1, 1);
	Butterfly(T264_i0, T264_i1, &T264_o0, &T264_o1, T264_W);
	PUT_FIFO(T264_o0, 0);
	PUT_FIFO(T264_o1, 1);

	GET_FIFO(T265_i0, 0);
	GET_FIFO(T265_i1, 1);
	Butterfly(T265_i0, T265_i1, &T265_o0, &T265_o1, T265_W);
	PUT_FIFO(T265_o0, 0);
	PUT_FIFO(T265_o1, 1);

	GET_FIFO(T266_i0, 0);
	GET_FIFO(T266_i1, 1);
	Butterfly(T266_i0, T266_i1, &T266_o0, &T266_o1, T266_W);
	PUT_FIFO(T266_o0, 2);
	PUT_FIFO(T266_o1, 3);

	GET_FIFO(T267_i0, 0);
	GET_FIFO(T267_i1, 1);
	Butterfly(T267_i0, T267_i1, &T267_o0, &T267_o1, T267_W);
	PUT_FIFO(T267_o0, 2);
	PUT_FIFO(T267_o1, 3);

	GET_FIFO(T268_i0, 0);
	GET_FIFO(T268_i1, 1);
	Butterfly(T268_i0, T268_i1, &T268_o0, &T268_o1, T268_W);
	PUT_FIFO(T268_o0, 0);
	PUT_FIFO(T268_o1, 1);

	GET_FIFO(T269_i0, 0);
	GET_FIFO(T269_i1, 1);
	Butterfly(T269_i0, T269_i1, &T269_o0, &T269_o1, T269_W);
	PUT_FIFO(T269_o0, 0);
	PUT_FIFO(T269_o1, 1);

	GET_FIFO(T270_i0, 0);
	GET_FIFO(T270_i1, 1);
	Butterfly(T270_i0, T270_i1, &T270_o0, &T270_o1, T270_W);
	PUT_FIFO(T270_o0, 2);
	PUT_FIFO(T270_o1, 3);

	GET_FIFO(T271_i0, 0);
	GET_FIFO(T271_i1, 1);
	Butterfly(T271_i0, T271_i1, &T271_o0, &T271_o1, T271_W);
	PUT_FIFO(T271_o0, 2);
	PUT_FIFO(T271_o1, 3);

	GET_FIFO(T272_i0, 0);
	GET_FIFO(T272_i1, 1);
	Butterfly(T272_i0, T272_i1, &T272_o0, &T272_o1, T272_W);
	PUT_FIFO(T272_o0, 0);
	PUT_FIFO(T272_o1, 1);

	GET_FIFO(T273_i0, 0);
	GET_FIFO(T273_i1, 1);
	Butterfly(T273_i0, T273_i1, &T273_o0, &T273_o1, T273_W);
	PUT_FIFO(T273_o0, 0);
	PUT_FIFO(T273_o1, 1);

	GET_FIFO(T274_i0, 0);
	GET_FIFO(T274_i1, 1);
	Butterfly(T274_i0, T274_i1, &T274_o0, &T274_o1, T274_W);
	PUT_FIFO(T274_o0, 2);
	PUT_FIFO(T274_o1, 3);

	GET_FIFO(T275_i0, 0);
	GET_FIFO(T275_i1, 1);
	Butterfly(T275_i0, T275_i1, &T275_o0, &T275_o1, T275_W);
	PUT_FIFO(T275_o0, 2);
	PUT_FIFO(T275_o1, 3);

	GET_FIFO(T276_i0, 0);
	GET_FIFO(T276_i1, 1);
	Butterfly(T276_i0, T276_i1, &T276_o0, &T276_o1, T276_W);
	PUT_FIFO(T276_o0, 0);
	PUT_FIFO(T276_o1, 1);

	GET_FIFO(T277_i0, 0);
	GET_FIFO(T277_i1, 1);
	Butterfly(T277_i0, T277_i1, &T277_o0, &T277_o1, T277_W);
	PUT_FIFO(T277_o0, 0);
	PUT_FIFO(T277_o1, 1);

	GET_FIFO(T278_i0, 0);
	GET_FIFO(T278_i1, 1);
	Butterfly(T278_i0, T278_i1, &T278_o0, &T278_o1, T278_W);
	PUT_FIFO(T278_o0, 2);
	PUT_FIFO(T278_o1, 3);

	GET_FIFO(T279_i0, 0);
	GET_FIFO(T279_i1, 1);
	Butterfly(T279_i0, T279_i1, &T279_o0, &T279_o1, T279_W);
	PUT_FIFO(T279_o0, 2);
	PUT_FIFO(T279_o1, 3);

	GET_FIFO(T280_i0, 0);
	GET_FIFO(T280_i1, 1);
	Butterfly(T280_i0, T280_i1, &T280_o0, &T280_o1, T280_W);
	PUT_FIFO(T280_o0, 0);
	PUT_FIFO(T280_o1, 1);

	GET_FIFO(T281_i0, 0);
	GET_FIFO(T281_i1, 1);
	Butterfly(T281_i0, T281_i1, &T281_o0, &T281_o1, T281_W);
	PUT_FIFO(T281_o0, 0);
	PUT_FIFO(T281_o1, 1);

	GET_FIFO(T282_i0, 0);
	GET_FIFO(T282_i1, 1);
	Butterfly(T282_i0, T282_i1, &T282_o0, &T282_o1, T282_W);
	PUT_FIFO(T282_o0, 2);
	PUT_FIFO(T282_o1, 3);

	GET_FIFO(T283_i0, 0);
	GET_FIFO(T283_i1, 1);
	Butterfly(T283_i0, T283_i1, &T283_o0, &T283_o1, T283_W);
	PUT_FIFO(T283_o0, 2);
	PUT_FIFO(T283_o1, 3);

	GET_FIFO(T284_i0, 0);
	GET_FIFO(T284_i1, 1);
	Butterfly(T284_i0, T284_i1, &T284_o0, &T284_o1, T284_W);
	PUT_FIFO(T284_o0, 0);
	PUT_FIFO(T284_o1, 1);

	GET_FIFO(T285_i0, 0);
	GET_FIFO(T285_i1, 1);
	Butterfly(T285_i0, T285_i1, &T285_o0, &T285_o1, T285_W);
	PUT_FIFO(T285_o0, 0);
	PUT_FIFO(T285_o1, 1);

	GET_FIFO(T286_i0, 0);
	GET_FIFO(T286_i1, 1);
	Butterfly(T286_i0, T286_i1, &T286_o0, &T286_o1, T286_W);
	PUT_FIFO(T286_o0, 2);
	PUT_FIFO(T286_o1, 3);

	GET_FIFO(T287_i0, 0);
	GET_FIFO(T287_i1, 1);
	Butterfly(T287_i0, T287_i1, &T287_o0, &T287_o1, T287_W);
	PUT_FIFO(T287_o0, 2);
	PUT_FIFO(T287_o1, 3);

	GET_FIFO(T288_i0, 0);
	GET_FIFO(T288_i1, 1);
	Butterfly(T288_i0, T288_i1, &T288_o0, &T288_o1, T288_W);
	PUT_FIFO(T288_o0, 0);
	PUT_FIFO(T288_o1, 1);

	GET_FIFO(T289_i0, 0);
	GET_FIFO(T289_i1, 1);
	Butterfly(T289_i0, T289_i1, &T289_o0, &T289_o1, T289_W);
	PUT_FIFO(T289_o0, 0);
	PUT_FIFO(T289_o1, 1);

	GET_FIFO(T290_i0, 0);
	GET_FIFO(T290_i1, 1);
	Butterfly(T290_i0, T290_i1, &T290_o0, &T290_o1, T290_W);
	PUT_FIFO(T290_o0, 2);
	PUT_FIFO(T290_o1, 3);

	GET_FIFO(T291_i0, 0);
	GET_FIFO(T291_i1, 1);
	Butterfly(T291_i0, T291_i1, &T291_o0, &T291_o1, T291_W);
	PUT_FIFO(T291_o0, 2);
	PUT_FIFO(T291_o1, 3);

	GET_FIFO(T292_i0, 0);
	GET_FIFO(T292_i1, 1);
	Butterfly(T292_i0, T292_i1, &T292_o0, &T292_o1, T292_W);
	PUT_FIFO(T292_o0, 0);
	PUT_FIFO(T292_o1, 1);

	GET_FIFO(T293_i0, 0);
	GET_FIFO(T293_i1, 1);
	Butterfly(T293_i0, T293_i1, &T293_o0, &T293_o1, T293_W);
	PUT_FIFO(T293_o0, 0);
	PUT_FIFO(T293_o1, 1);

	GET_FIFO(T294_i0, 0);
	GET_FIFO(T294_i1, 1);
	Butterfly(T294_i0, T294_i1, &T294_o0, &T294_o1, T294_W);
	PUT_FIFO(T294_o0, 2);
	PUT_FIFO(T294_o1, 3);

	GET_FIFO(T295_i0, 0);
	GET_FIFO(T295_i1, 1);
	Butterfly(T295_i0, T295_i1, &T295_o0, &T295_o1, T295_W);
	PUT_FIFO(T295_o0, 2);
	PUT_FIFO(T295_o1, 3);

	GET_FIFO(T296_i0, 0);
	GET_FIFO(T296_i1, 1);
	Butterfly(T296_i0, T296_i1, &T296_o0, &T296_o1, T296_W);
	PUT_FIFO(T296_o0, 0);
	PUT_FIFO(T296_o1, 1);

	GET_FIFO(T297_i0, 0);
	GET_FIFO(T297_i1, 1);
	Butterfly(T297_i0, T297_i1, &T297_o0, &T297_o1, T297_W);
	PUT_FIFO(T297_o0, 0);
	PUT_FIFO(T297_o1, 1);

	GET_FIFO(T298_i0, 0);
	GET_FIFO(T298_i1, 1);
	Butterfly(T298_i0, T298_i1, &T298_o0, &T298_o1, T298_W);
	PUT_FIFO(T298_o0, 2);
	PUT_FIFO(T298_o1, 3);

	GET_FIFO(T299_i0, 0);
	GET_FIFO(T299_i1, 1);
	Butterfly(T299_i0, T299_i1, &T299_o0, &T299_o1, T299_W);
	PUT_FIFO(T299_o0, 2);
	PUT_FIFO(T299_o1, 3);

	GET_FIFO(T300_i0, 0);
	GET_FIFO(T300_i1, 1);
	Butterfly(T300_i0, T300_i1, &T300_o0, &T300_o1, T300_W);
	PUT_FIFO(T300_o0, 0);
	PUT_FIFO(T300_o1, 1);

	GET_FIFO(T301_i0, 0);
	GET_FIFO(T301_i1, 1);
	Butterfly(T301_i0, T301_i1, &T301_o0, &T301_o1, T301_W);
	PUT_FIFO(T301_o0, 0);
	PUT_FIFO(T301_o1, 1);

	GET_FIFO(T302_i0, 0);
	GET_FIFO(T302_i1, 1);
	Butterfly(T302_i0, T302_i1, &T302_o0, &T302_o1, T302_W);
	PUT_FIFO(T302_o0, 2);
	PUT_FIFO(T302_o1, 3);

	GET_FIFO(T303_i0, 0);
	GET_FIFO(T303_i1, 1);
	Butterfly(T303_i0, T303_i1, &T303_o0, &T303_o1, T303_W);
	PUT_FIFO(T303_o0, 2);
	PUT_FIFO(T303_o1, 3);

	GET_FIFO(T304_i0, 0);
	GET_FIFO(T304_i1, 1);
	Butterfly(T304_i0, T304_i1, &T304_o0, &T304_o1, T304_W);
	PUT_FIFO(T304_o0, 0);
	PUT_FIFO(T304_o1, 1);

	GET_FIFO(T305_i0, 0);
	GET_FIFO(T305_i1, 1);
	Butterfly(T305_i0, T305_i1, &T305_o0, &T305_o1, T305_W);
	PUT_FIFO(T305_o0, 0);
	PUT_FIFO(T305_o1, 1);

	GET_FIFO(T306_i0, 0);
	GET_FIFO(T306_i1, 1);
	Butterfly(T306_i0, T306_i1, &T306_o0, &T306_o1, T306_W);
	PUT_FIFO(T306_o0, 2);
	PUT_FIFO(T306_o1, 3);

	GET_FIFO(T307_i0, 0);
	GET_FIFO(T307_i1, 1);
	Butterfly(T307_i0, T307_i1, &T307_o0, &T307_o1, T307_W);
	PUT_FIFO(T307_o0, 2);
	PUT_FIFO(T307_o1, 3);

	GET_FIFO(T308_i0, 0);
	GET_FIFO(T308_i1, 1);
	Butterfly(T308_i0, T308_i1, &T308_o0, &T308_o1, T308_W);
	PUT_FIFO(T308_o0, 0);
	PUT_FIFO(T308_o1, 1);

	GET_FIFO(T309_i0, 0);
	GET_FIFO(T309_i1, 1);
	Butterfly(T309_i0, T309_i1, &T309_o0, &T309_o1, T309_W);
	PUT_FIFO(T309_o0, 0);
	PUT_FIFO(T309_o1, 1);

	GET_FIFO(T310_i0, 0);
	GET_FIFO(T310_i1, 1);
	Butterfly(T310_i0, T310_i1, &T310_o0, &T310_o1, T310_W);
	PUT_FIFO(T310_o0, 2);
	PUT_FIFO(T310_o1, 3);

	GET_FIFO(T311_i0, 0);
	GET_FIFO(T311_i1, 1);
	Butterfly(T311_i0, T311_i1, &T311_o0, &T311_o1, T311_W);
	PUT_FIFO(T311_o0, 2);
	PUT_FIFO(T311_o1, 3);

	GET_FIFO(T312_i0, 0);
	GET_FIFO(T312_i1, 1);
	Butterfly(T312_i0, T312_i1, &T312_o0, &T312_o1, T312_W);
	PUT_FIFO(T312_o0, 0);
	PUT_FIFO(T312_o1, 1);

	GET_FIFO(T313_i0, 0);
	GET_FIFO(T313_i1, 1);
	Butterfly(T313_i0, T313_i1, &T313_o0, &T313_o1, T313_W);
	PUT_FIFO(T313_o0, 0);
	PUT_FIFO(T313_o1, 1);

	GET_FIFO(T314_i0, 0);
	GET_FIFO(T314_i1, 1);
	Butterfly(T314_i0, T314_i1, &T314_o0, &T314_o1, T314_W);
	PUT_FIFO(T314_o0, 2);
	PUT_FIFO(T314_o1, 3);

	GET_FIFO(T315_i0, 0);
	GET_FIFO(T315_i1, 1);
	Butterfly(T315_i0, T315_i1, &T315_o0, &T315_o1, T315_W);
	PUT_FIFO(T315_o0, 2);
	PUT_FIFO(T315_o1, 3);

	GET_FIFO(T316_i0, 0);
	GET_FIFO(T316_i1, 1);
	Butterfly(T316_i0, T316_i1, &T316_o0, &T316_o1, T316_W);
	PUT_FIFO(T316_o0, 0);
	PUT_FIFO(T316_o1, 1);

	GET_FIFO(T317_i0, 0);
	GET_FIFO(T317_i1, 1);
	Butterfly(T317_i0, T317_i1, &T317_o0, &T317_o1, T317_W);
	PUT_FIFO(T317_o0, 0);
	PUT_FIFO(T317_o1, 1);

	GET_FIFO(T318_i0, 0);
	GET_FIFO(T318_i1, 1);
	Butterfly(T318_i0, T318_i1, &T318_o0, &T318_o1, T318_W);
	PUT_FIFO(T318_o0, 2);
	PUT_FIFO(T318_o1, 3);

	GET_FIFO(T319_i0, 0);
	GET_FIFO(T319_i1, 1);
	Butterfly(T319_i0, T319_i1, &T319_o0, &T319_o1, T319_W);
	PUT_FIFO(T319_o0, 2);
	PUT_FIFO(T319_o1, 3);

	GET_FIFO(T320_i0, 0);
	GET_FIFO(T320_i1, 1);
	Butterfly(T320_i0, T320_i1, &T320_o0, &T320_o1, T320_W);
	PUT_FIFO(T320_o0, 0);
	PUT_FIFO(T320_o1, 1);

	GET_FIFO(T321_i0, 0);
	GET_FIFO(T321_i1, 1);
	Butterfly(T321_i0, T321_i1, &T321_o0, &T321_o1, T321_W);
	PUT_FIFO(T321_o0, 0);
	PUT_FIFO(T321_o1, 1);

	GET_FIFO(T322_i0, 0);
	GET_FIFO(T322_i1, 1);
	Butterfly(T322_i0, T322_i1, &T322_o0, &T322_o1, T322_W);
	PUT_FIFO(T322_o0, 2);
	PUT_FIFO(T322_o1, 3);

	GET_FIFO(T323_i0, 0);
	GET_FIFO(T323_i1, 1);
	Butterfly(T323_i0, T323_i1, &T323_o0, &T323_o1, T323_W);
	PUT_FIFO(T323_o0, 2);
	PUT_FIFO(T323_o1, 3);

	GET_FIFO(T324_i0, 0);
	GET_FIFO(T324_i1, 1);
	Butterfly(T324_i0, T324_i1, &T324_o0, &T324_o1, T324_W);
	PUT_FIFO(T324_o0, 0);
	PUT_FIFO(T324_o1, 1);

	GET_FIFO(T325_i0, 0);
	GET_FIFO(T325_i1, 1);
	Butterfly(T325_i0, T325_i1, &T325_o0, &T325_o1, T325_W);
	PUT_FIFO(T325_o0, 0);
	PUT_FIFO(T325_o1, 1);

	GET_FIFO(T326_i0, 0);
	GET_FIFO(T326_i1, 1);
	Butterfly(T326_i0, T326_i1, &T326_o0, &T326_o1, T326_W);
	PUT_FIFO(T326_o0, 2);
	PUT_FIFO(T326_o1, 3);

	GET_FIFO(T327_i0, 0);
	GET_FIFO(T327_i1, 1);
	Butterfly(T327_i0, T327_i1, &T327_o0, &T327_o1, T327_W);
	PUT_FIFO(T327_o0, 2);
	PUT_FIFO(T327_o1, 3);

	GET_FIFO(T328_i0, 0);
	GET_FIFO(T328_i1, 1);
	Butterfly(T328_i0, T328_i1, &T328_o0, &T328_o1, T328_W);
	PUT_FIFO(T328_o0, 0);
	PUT_FIFO(T328_o1, 1);

	GET_FIFO(T329_i0, 0);
	GET_FIFO(T329_i1, 1);
	Butterfly(T329_i0, T329_i1, &T329_o0, &T329_o1, T329_W);
	PUT_FIFO(T329_o0, 0);
	PUT_FIFO(T329_o1, 1);

	GET_FIFO(T330_i0, 0);
	GET_FIFO(T330_i1, 1);
	Butterfly(T330_i0, T330_i1, &T330_o0, &T330_o1, T330_W);
	PUT_FIFO(T330_o0, 2);
	PUT_FIFO(T330_o1, 3);

	GET_FIFO(T331_i0, 0);
	GET_FIFO(T331_i1, 1);
	Butterfly(T331_i0, T331_i1, &T331_o0, &T331_o1, T331_W);
	PUT_FIFO(T331_o0, 2);
	PUT_FIFO(T331_o1, 3);

	GET_FIFO(T332_i0, 0);
	GET_FIFO(T332_i1, 1);
	Butterfly(T332_i0, T332_i1, &T332_o0, &T332_o1, T332_W);
	PUT_FIFO(T332_o0, 0);
	PUT_FIFO(T332_o1, 1);

	GET_FIFO(T333_i0, 0);
	GET_FIFO(T333_i1, 1);
	Butterfly(T333_i0, T333_i1, &T333_o0, &T333_o1, T333_W);
	PUT_FIFO(T333_o0, 0);
	PUT_FIFO(T333_o1, 1);

	GET_FIFO(T334_i0, 0);
	GET_FIFO(T334_i1, 1);
	Butterfly(T334_i0, T334_i1, &T334_o0, &T334_o1, T334_W);
	PUT_FIFO(T334_o0, 2);
	PUT_FIFO(T334_o1, 3);

	GET_FIFO(T335_i0, 0);
	GET_FIFO(T335_i1, 1);
	Butterfly(T335_i0, T335_i1, &T335_o0, &T335_o1, T335_W);
	PUT_FIFO(T335_o0, 2);
	PUT_FIFO(T335_o1, 3);

	GET_FIFO(T336_i0, 0);
	GET_FIFO(T336_i1, 1);
	Butterfly(T336_i0, T336_i1, &T336_o0, &T336_o1, T336_W);
	PUT_FIFO(T336_o0, 0);
	PUT_FIFO(T336_o1, 1);

	GET_FIFO(T337_i0, 0);
	GET_FIFO(T337_i1, 1);
	Butterfly(T337_i0, T337_i1, &T337_o0, &T337_o1, T337_W);
	PUT_FIFO(T337_o0, 0);
	PUT_FIFO(T337_o1, 1);

	GET_FIFO(T338_i0, 0);
	GET_FIFO(T338_i1, 1);
	Butterfly(T338_i0, T338_i1, &T338_o0, &T338_o1, T338_W);
	PUT_FIFO(T338_o0, 2);
	PUT_FIFO(T338_o1, 3);

	GET_FIFO(T339_i0, 0);
	GET_FIFO(T339_i1, 1);
	Butterfly(T339_i0, T339_i1, &T339_o0, &T339_o1, T339_W);
	PUT_FIFO(T339_o0, 2);
	PUT_FIFO(T339_o1, 3);

	GET_FIFO(T340_i0, 0);
	GET_FIFO(T340_i1, 1);
	Butterfly(T340_i0, T340_i1, &T340_o0, &T340_o1, T340_W);
	PUT_FIFO(T340_o0, 0);
	PUT_FIFO(T340_o1, 1);

	GET_FIFO(T341_i0, 0);
	GET_FIFO(T341_i1, 1);
	Butterfly(T341_i0, T341_i1, &T341_o0, &T341_o1, T341_W);
	PUT_FIFO(T341_o0, 0);
	PUT_FIFO(T341_o1, 1);

	GET_FIFO(T342_i0, 0);
	GET_FIFO(T342_i1, 1);
	Butterfly(T342_i0, T342_i1, &T342_o0, &T342_o1, T342_W);
	PUT_FIFO(T342_o0, 2);
	PUT_FIFO(T342_o1, 3);

	GET_FIFO(T343_i0, 0);
	GET_FIFO(T343_i1, 1);
	Butterfly(T343_i0, T343_i1, &T343_o0, &T343_o1, T343_W);
	PUT_FIFO(T343_o0, 2);
	PUT_FIFO(T343_o1, 3);

	GET_FIFO(T344_i0, 0);
	GET_FIFO(T344_i1, 1);
	Butterfly(T344_i0, T344_i1, &T344_o0, &T344_o1, T344_W);
	PUT_FIFO(T344_o0, 0);
	PUT_FIFO(T344_o1, 1);

	GET_FIFO(T345_i0, 0);
	GET_FIFO(T345_i1, 1);
	Butterfly(T345_i0, T345_i1, &T345_o0, &T345_o1, T345_W);
	PUT_FIFO(T345_o0, 0);
	PUT_FIFO(T345_o1, 1);

	GET_FIFO(T346_i0, 0);
	GET_FIFO(T346_i1, 1);
	Butterfly(T346_i0, T346_i1, &T346_o0, &T346_o1, T346_W);
	PUT_FIFO(T346_o0, 2);
	PUT_FIFO(T346_o1, 3);

	GET_FIFO(T347_i0, 0);
	GET_FIFO(T347_i1, 1);
	Butterfly(T347_i0, T347_i1, &T347_o0, &T347_o1, T347_W);
	PUT_FIFO(T347_o0, 2);
	PUT_FIFO(T347_o1, 3);

	GET_FIFO(T348_i0, 0);
	GET_FIFO(T348_i1, 1);
	Butterfly(T348_i0, T348_i1, &T348_o0, &T348_o1, T348_W);
	PUT_FIFO(T348_o0, 0);
	PUT_FIFO(T348_o1, 1);

	GET_FIFO(T349_i0, 0);
	GET_FIFO(T349_i1, 1);
	Butterfly(T349_i0, T349_i1, &T349_o0, &T349_o1, T349_W);
	PUT_FIFO(T349_o0, 0);
	PUT_FIFO(T349_o1, 1);

	GET_FIFO(T350_i0, 0);
	GET_FIFO(T350_i1, 1);
	Butterfly(T350_i0, T350_i1, &T350_o0, &T350_o1, T350_W);
	PUT_FIFO(T350_o0, 2);
	PUT_FIFO(T350_o1, 3);

	GET_FIFO(T351_i0, 0);
	GET_FIFO(T351_i1, 1);
	Butterfly(T351_i0, T351_i1, &T351_o0, &T351_o1, T351_W);
	PUT_FIFO(T351_o0, 2);
	PUT_FIFO(T351_o1, 3);

	GET_FIFO(T352_i0, 0);
	GET_FIFO(T352_i1, 1);
	Butterfly(T352_i0, T352_i1, &T352_o0, &T352_o1, T352_W);
	PUT_FIFO(T352_o0, 0);
	PUT_FIFO(T352_o1, 1);

	GET_FIFO(T353_i0, 0);
	GET_FIFO(T353_i1, 1);
	Butterfly(T353_i0, T353_i1, &T353_o0, &T353_o1, T353_W);
	PUT_FIFO(T353_o0, 0);
	PUT_FIFO(T353_o1, 1);

	GET_FIFO(T354_i0, 0);
	GET_FIFO(T354_i1, 1);
	Butterfly(T354_i0, T354_i1, &T354_o0, &T354_o1, T354_W);
	PUT_FIFO(T354_o0, 2);
	PUT_FIFO(T354_o1, 3);

	GET_FIFO(T355_i0, 0);
	GET_FIFO(T355_i1, 1);
	Butterfly(T355_i0, T355_i1, &T355_o0, &T355_o1, T355_W);
	PUT_FIFO(T355_o0, 2);
	PUT_FIFO(T355_o1, 3);

	GET_FIFO(T356_i0, 0);
	GET_FIFO(T356_i1, 1);
	Butterfly(T356_i0, T356_i1, &T356_o0, &T356_o1, T356_W);
	PUT_FIFO(T356_o0, 0);
	PUT_FIFO(T356_o1, 1);

	GET_FIFO(T357_i0, 0);
	GET_FIFO(T357_i1, 1);
	Butterfly(T357_i0, T357_i1, &T357_o0, &T357_o1, T357_W);
	PUT_FIFO(T357_o0, 0);
	PUT_FIFO(T357_o1, 1);

	GET_FIFO(T358_i0, 0);
	GET_FIFO(T358_i1, 1);
	Butterfly(T358_i0, T358_i1, &T358_o0, &T358_o1, T358_W);
	PUT_FIFO(T358_o0, 2);
	PUT_FIFO(T358_o1, 3);

	GET_FIFO(T359_i0, 0);
	GET_FIFO(T359_i1, 1);
	Butterfly(T359_i0, T359_i1, &T359_o0, &T359_o1, T359_W);
	PUT_FIFO(T359_o0, 2);
	PUT_FIFO(T359_o1, 3);

	GET_FIFO(T360_i0, 0);
	GET_FIFO(T360_i1, 1);
	Butterfly(T360_i0, T360_i1, &T360_o0, &T360_o1, T360_W);
	PUT_FIFO(T360_o0, 0);
	PUT_FIFO(T360_o1, 1);

	GET_FIFO(T361_i0, 0);
	GET_FIFO(T361_i1, 1);
	Butterfly(T361_i0, T361_i1, &T361_o0, &T361_o1, T361_W);
	PUT_FIFO(T361_o0, 0);
	PUT_FIFO(T361_o1, 1);

	GET_FIFO(T362_i0, 0);
	GET_FIFO(T362_i1, 1);
	Butterfly(T362_i0, T362_i1, &T362_o0, &T362_o1, T362_W);
	PUT_FIFO(T362_o0, 2);
	PUT_FIFO(T362_o1, 3);

	GET_FIFO(T363_i0, 0);
	GET_FIFO(T363_i1, 1);
	Butterfly(T363_i0, T363_i1, &T363_o0, &T363_o1, T363_W);
	PUT_FIFO(T363_o0, 2);
	PUT_FIFO(T363_o1, 3);

	GET_FIFO(T364_i0, 0);
	GET_FIFO(T364_i1, 1);
	Butterfly(T364_i0, T364_i1, &T364_o0, &T364_o1, T364_W);
	PUT_FIFO(T364_o0, 0);
	PUT_FIFO(T364_o1, 1);

	GET_FIFO(T365_i0, 0);
	GET_FIFO(T365_i1, 1);
	Butterfly(T365_i0, T365_i1, &T365_o0, &T365_o1, T365_W);
	PUT_FIFO(T365_o0, 0);
	PUT_FIFO(T365_o1, 1);

	GET_FIFO(T366_i0, 0);
	GET_FIFO(T366_i1, 1);
	Butterfly(T366_i0, T366_i1, &T366_o0, &T366_o1, T366_W);
	PUT_FIFO(T366_o0, 2);
	PUT_FIFO(T366_o1, 3);

	GET_FIFO(T367_i0, 0);
	GET_FIFO(T367_i1, 1);
	Butterfly(T367_i0, T367_i1, &T367_o0, &T367_o1, T367_W);
	PUT_FIFO(T367_o0, 2);
	PUT_FIFO(T367_o1, 3);

	GET_FIFO(T368_i0, 0);
	GET_FIFO(T368_i1, 1);
	Butterfly(T368_i0, T368_i1, &T368_o0, &T368_o1, T368_W);
	PUT_FIFO(T368_o0, 0);
	PUT_FIFO(T368_o1, 1);

	GET_FIFO(T369_i0, 0);
	GET_FIFO(T369_i1, 1);
	Butterfly(T369_i0, T369_i1, &T369_o0, &T369_o1, T369_W);
	PUT_FIFO(T369_o0, 0);
	PUT_FIFO(T369_o1, 1);

	GET_FIFO(T370_i0, 0);
	GET_FIFO(T370_i1, 1);
	Butterfly(T370_i0, T370_i1, &T370_o0, &T370_o1, T370_W);
	PUT_FIFO(T370_o0, 2);
	PUT_FIFO(T370_o1, 3);

	GET_FIFO(T371_i0, 0);
	GET_FIFO(T371_i1, 1);
	Butterfly(T371_i0, T371_i1, &T371_o0, &T371_o1, T371_W);
	PUT_FIFO(T371_o0, 2);
	PUT_FIFO(T371_o1, 3);

	GET_FIFO(T372_i0, 0);
	GET_FIFO(T372_i1, 1);
	Butterfly(T372_i0, T372_i1, &T372_o0, &T372_o1, T372_W);
	PUT_FIFO(T372_o0, 0);
	PUT_FIFO(T372_o1, 1);

	GET_FIFO(T373_i0, 0);
	GET_FIFO(T373_i1, 1);
	Butterfly(T373_i0, T373_i1, &T373_o0, &T373_o1, T373_W);
	PUT_FIFO(T373_o0, 0);
	PUT_FIFO(T373_o1, 1);

	GET_FIFO(T374_i0, 0);
	GET_FIFO(T374_i1, 1);
	Butterfly(T374_i0, T374_i1, &T374_o0, &T374_o1, T374_W);
	PUT_FIFO(T374_o0, 2);
	PUT_FIFO(T374_o1, 3);

	GET_FIFO(T375_i0, 0);
	GET_FIFO(T375_i1, 1);
	Butterfly(T375_i0, T375_i1, &T375_o0, &T375_o1, T375_W);
	PUT_FIFO(T375_o0, 2);
	PUT_FIFO(T375_o1, 3);

	GET_FIFO(T376_i0, 0);
	GET_FIFO(T376_i1, 1);
	Butterfly(T376_i0, T376_i1, &T376_o0, &T376_o1, T376_W);
	PUT_FIFO(T376_o0, 0);
	PUT_FIFO(T376_o1, 1);

	GET_FIFO(T377_i0, 0);
	GET_FIFO(T377_i1, 1);
	Butterfly(T377_i0, T377_i1, &T377_o0, &T377_o1, T377_W);
	PUT_FIFO(T377_o0, 0);
	PUT_FIFO(T377_o1, 1);

	GET_FIFO(T378_i0, 0);
	GET_FIFO(T378_i1, 1);
	Butterfly(T378_i0, T378_i1, &T378_o0, &T378_o1, T378_W);
	PUT_FIFO(T378_o0, 2);
	PUT_FIFO(T378_o1, 3);

	GET_FIFO(T379_i0, 0);
	GET_FIFO(T379_i1, 1);
	Butterfly(T379_i0, T379_i1, &T379_o0, &T379_o1, T379_W);
	PUT_FIFO(T379_o0, 2);
	PUT_FIFO(T379_o1, 3);

	GET_FIFO(T380_i0, 0);
	GET_FIFO(T380_i1, 1);
	Butterfly(T380_i0, T380_i1, &T380_o0, &T380_o1, T380_W);
	PUT_FIFO(T380_o0, 0);
	PUT_FIFO(T380_o1, 1);

	GET_FIFO(T381_i0, 0);
	GET_FIFO(T381_i1, 1);
	Butterfly(T381_i0, T381_i1, &T381_o0, &T381_o1, T381_W);
	PUT_FIFO(T381_o0, 0);
	PUT_FIFO(T381_o1, 1);

	GET_FIFO(T382_i0, 0);
	GET_FIFO(T382_i1, 1);
	Butterfly(T382_i0, T382_i1, &T382_o0, &T382_o1, T382_W);
	PUT_FIFO(T382_o0, 2);
	PUT_FIFO(T382_o1, 3);

	GET_FIFO(T383_i0, 0);
	GET_FIFO(T383_i1, 1);
	Butterfly(T383_i0, T383_i1, &T383_o0, &T383_o1, T383_W);
	PUT_FIFO(T383_o0, 2);
	PUT_FIFO(T383_o1, 3);

	GET_FIFO(T384_i0, 0);
	GET_FIFO(T384_i1, 1);
	Butterfly(T384_i0, T384_i1, &T384_o0, &T384_o1, T384_W);
	PUT_FIFO(T384_o0, 0);
	PUT_FIFO(T384_o1, 1);

	GET_FIFO(T385_i0, 0);
	GET_FIFO(T385_i1, 1);
	Butterfly(T385_i0, T385_i1, &T385_o0, &T385_o1, T385_W);
	PUT_FIFO(T385_o0, 0);
	PUT_FIFO(T385_o1, 1);

	GET_FIFO(T386_i0, 0);
	GET_FIFO(T386_i1, 1);
	Butterfly(T386_i0, T386_i1, &T386_o0, &T386_o1, T386_W);
	PUT_FIFO(T386_o0, 2);
	PUT_FIFO(T386_o1, 3);

	GET_FIFO(T387_i0, 0);
	GET_FIFO(T387_i1, 1);
	Butterfly(T387_i0, T387_i1, &T387_o0, &T387_o1, T387_W);
	PUT_FIFO(T387_o0, 2);
	PUT_FIFO(T387_o1, 3);

	GET_FIFO(T388_i0, 0);
	GET_FIFO(T388_i1, 1);
	Butterfly(T388_i0, T388_i1, &T388_o0, &T388_o1, T388_W);
	PUT_FIFO(T388_o0, 0);
	PUT_FIFO(T388_o1, 1);

	GET_FIFO(T389_i0, 0);
	GET_FIFO(T389_i1, 1);
	Butterfly(T389_i0, T389_i1, &T389_o0, &T389_o1, T389_W);
	PUT_FIFO(T389_o0, 0);
	PUT_FIFO(T389_o1, 1);

	GET_FIFO(T390_i0, 0);
	GET_FIFO(T390_i1, 1);
	Butterfly(T390_i0, T390_i1, &T390_o0, &T390_o1, T390_W);
	PUT_FIFO(T390_o0, 2);
	PUT_FIFO(T390_o1, 3);

	GET_FIFO(T391_i0, 0);
	GET_FIFO(T391_i1, 1);
	Butterfly(T391_i0, T391_i1, &T391_o0, &T391_o1, T391_W);
	PUT_FIFO(T391_o0, 2);
	PUT_FIFO(T391_o1, 3);

	GET_FIFO(T392_i0, 0);
	GET_FIFO(T392_i1, 1);
	Butterfly(T392_i0, T392_i1, &T392_o0, &T392_o1, T392_W);
	PUT_FIFO(T392_o0, 0);
	PUT_FIFO(T392_o1, 1);

	GET_FIFO(T393_i0, 0);
	GET_FIFO(T393_i1, 1);
	Butterfly(T393_i0, T393_i1, &T393_o0, &T393_o1, T393_W);
	PUT_FIFO(T393_o0, 0);
	PUT_FIFO(T393_o1, 1);

	GET_FIFO(T394_i0, 0);
	GET_FIFO(T394_i1, 1);
	Butterfly(T394_i0, T394_i1, &T394_o0, &T394_o1, T394_W);
	PUT_FIFO(T394_o0, 2);
	PUT_FIFO(T394_o1, 3);

	GET_FIFO(T395_i0, 0);
	GET_FIFO(T395_i1, 1);
	Butterfly(T395_i0, T395_i1, &T395_o0, &T395_o1, T395_W);
	PUT_FIFO(T395_o0, 2);
	PUT_FIFO(T395_o1, 3);

	GET_FIFO(T396_i0, 0);
	GET_FIFO(T396_i1, 1);
	Butterfly(T396_i0, T396_i1, &T396_o0, &T396_o1, T396_W);
	PUT_FIFO(T396_o0, 0);
	PUT_FIFO(T396_o1, 1);

	GET_FIFO(T397_i0, 0);
	GET_FIFO(T397_i1, 1);
	Butterfly(T397_i0, T397_i1, &T397_o0, &T397_o1, T397_W);
	PUT_FIFO(T397_o0, 0);
	PUT_FIFO(T397_o1, 1);

	GET_FIFO(T398_i0, 0);
	GET_FIFO(T398_i1, 1);
	Butterfly(T398_i0, T398_i1, &T398_o0, &T398_o1, T398_W);
	PUT_FIFO(T398_o0, 2);
	PUT_FIFO(T398_o1, 3);

	GET_FIFO(T399_i0, 0);
	GET_FIFO(T399_i1, 1);
	Butterfly(T399_i0, T399_i1, &T399_o0, &T399_o1, T399_W);
	PUT_FIFO(T399_o0, 2);
	PUT_FIFO(T399_o1, 3);

	GET_FIFO(T400_i0, 0);
	GET_FIFO(T400_i1, 1);
	Butterfly(T400_i0, T400_i1, &T400_o0, &T400_o1, T400_W);
	PUT_FIFO(T400_o0, 0);
	PUT_FIFO(T400_o1, 1);

	GET_FIFO(T401_i0, 0);
	GET_FIFO(T401_i1, 1);
	Butterfly(T401_i0, T401_i1, &T401_o0, &T401_o1, T401_W);
	PUT_FIFO(T401_o0, 0);
	PUT_FIFO(T401_o1, 1);

	GET_FIFO(T402_i0, 0);
	GET_FIFO(T402_i1, 1);
	Butterfly(T402_i0, T402_i1, &T402_o0, &T402_o1, T402_W);
	PUT_FIFO(T402_o0, 2);
	PUT_FIFO(T402_o1, 3);

	GET_FIFO(T403_i0, 0);
	GET_FIFO(T403_i1, 1);
	Butterfly(T403_i0, T403_i1, &T403_o0, &T403_o1, T403_W);
	PUT_FIFO(T403_o0, 2);
	PUT_FIFO(T403_o1, 3);

	GET_FIFO(T404_i0, 0);
	GET_FIFO(T404_i1, 1);
	Butterfly(T404_i0, T404_i1, &T404_o0, &T404_o1, T404_W);
	PUT_FIFO(T404_o0, 0);
	PUT_FIFO(T404_o1, 1);

	GET_FIFO(T405_i0, 0);
	GET_FIFO(T405_i1, 1);
	Butterfly(T405_i0, T405_i1, &T405_o0, &T405_o1, T405_W);
	PUT_FIFO(T405_o0, 0);
	PUT_FIFO(T405_o1, 1);

	GET_FIFO(T406_i0, 0);
	GET_FIFO(T406_i1, 1);
	Butterfly(T406_i0, T406_i1, &T406_o0, &T406_o1, T406_W);
	PUT_FIFO(T406_o0, 2);
	PUT_FIFO(T406_o1, 3);

	GET_FIFO(T407_i0, 0);
	GET_FIFO(T407_i1, 1);
	Butterfly(T407_i0, T407_i1, &T407_o0, &T407_o1, T407_W);
	PUT_FIFO(T407_o0, 2);
	PUT_FIFO(T407_o1, 3);

	GET_FIFO(T408_i0, 0);
	GET_FIFO(T408_i1, 1);
	Butterfly(T408_i0, T408_i1, &T408_o0, &T408_o1, T408_W);
	PUT_FIFO(T408_o0, 0);
	PUT_FIFO(T408_o1, 1);

	GET_FIFO(T409_i0, 0);
	GET_FIFO(T409_i1, 1);
	Butterfly(T409_i0, T409_i1, &T409_o0, &T409_o1, T409_W);
	PUT_FIFO(T409_o0, 0);
	PUT_FIFO(T409_o1, 1);

	GET_FIFO(T410_i0, 0);
	GET_FIFO(T410_i1, 1);
	Butterfly(T410_i0, T410_i1, &T410_o0, &T410_o1, T410_W);
	PUT_FIFO(T410_o0, 2);
	PUT_FIFO(T410_o1, 3);

	GET_FIFO(T411_i0, 0);
	GET_FIFO(T411_i1, 1);
	Butterfly(T411_i0, T411_i1, &T411_o0, &T411_o1, T411_W);
	PUT_FIFO(T411_o0, 2);
	PUT_FIFO(T411_o1, 3);

	GET_FIFO(T412_i0, 0);
	GET_FIFO(T412_i1, 1);
	Butterfly(T412_i0, T412_i1, &T412_o0, &T412_o1, T412_W);
	PUT_FIFO(T412_o0, 0);
	PUT_FIFO(T412_o1, 1);

	GET_FIFO(T413_i0, 0);
	GET_FIFO(T413_i1, 1);
	Butterfly(T413_i0, T413_i1, &T413_o0, &T413_o1, T413_W);
	PUT_FIFO(T413_o0, 0);
	PUT_FIFO(T413_o1, 1);

	GET_FIFO(T414_i0, 0);
	GET_FIFO(T414_i1, 1);
	Butterfly(T414_i0, T414_i1, &T414_o0, &T414_o1, T414_W);
	PUT_FIFO(T414_o0, 2);
	PUT_FIFO(T414_o1, 3);

	GET_FIFO(T415_i0, 0);
	GET_FIFO(T415_i1, 1);
	Butterfly(T415_i0, T415_i1, &T415_o0, &T415_o1, T415_W);
	PUT_FIFO(T415_o0, 2);
	PUT_FIFO(T415_o1, 3);

	GET_FIFO(T416_i0, 0);
	GET_FIFO(T416_i1, 1);
	Butterfly(T416_i0, T416_i1, &T416_o0, &T416_o1, T416_W);
	PUT_FIFO(T416_o0, 0);
	PUT_FIFO(T416_o1, 1);

	GET_FIFO(T417_i0, 0);
	GET_FIFO(T417_i1, 1);
	Butterfly(T417_i0, T417_i1, &T417_o0, &T417_o1, T417_W);
	PUT_FIFO(T417_o0, 0);
	PUT_FIFO(T417_o1, 1);

	GET_FIFO(T418_i0, 0);
	GET_FIFO(T418_i1, 1);
	Butterfly(T418_i0, T418_i1, &T418_o0, &T418_o1, T418_W);
	PUT_FIFO(T418_o0, 2);
	PUT_FIFO(T418_o1, 3);

	GET_FIFO(T419_i0, 0);
	GET_FIFO(T419_i1, 1);
	Butterfly(T419_i0, T419_i1, &T419_o0, &T419_o1, T419_W);
	PUT_FIFO(T419_o0, 2);
	PUT_FIFO(T419_o1, 3);

	GET_FIFO(T420_i0, 0);
	GET_FIFO(T420_i1, 1);
	Butterfly(T420_i0, T420_i1, &T420_o0, &T420_o1, T420_W);
	PUT_FIFO(T420_o0, 0);
	PUT_FIFO(T420_o1, 1);

	GET_FIFO(T421_i0, 0);
	GET_FIFO(T421_i1, 1);
	Butterfly(T421_i0, T421_i1, &T421_o0, &T421_o1, T421_W);
	PUT_FIFO(T421_o0, 0);
	PUT_FIFO(T421_o1, 1);

	GET_FIFO(T422_i0, 0);
	GET_FIFO(T422_i1, 1);
	Butterfly(T422_i0, T422_i1, &T422_o0, &T422_o1, T422_W);
	PUT_FIFO(T422_o0, 2);
	PUT_FIFO(T422_o1, 3);

	GET_FIFO(T423_i0, 0);
	GET_FIFO(T423_i1, 1);
	Butterfly(T423_i0, T423_i1, &T423_o0, &T423_o1, T423_W);
	PUT_FIFO(T423_o0, 2);
	PUT_FIFO(T423_o1, 3);

	GET_FIFO(T424_i0, 0);
	GET_FIFO(T424_i1, 1);
	Butterfly(T424_i0, T424_i1, &T424_o0, &T424_o1, T424_W);
	PUT_FIFO(T424_o0, 0);
	PUT_FIFO(T424_o1, 1);

	GET_FIFO(T425_i0, 0);
	GET_FIFO(T425_i1, 1);
	Butterfly(T425_i0, T425_i1, &T425_o0, &T425_o1, T425_W);
	PUT_FIFO(T425_o0, 0);
	PUT_FIFO(T425_o1, 1);

	GET_FIFO(T426_i0, 0);
	GET_FIFO(T426_i1, 1);
	Butterfly(T426_i0, T426_i1, &T426_o0, &T426_o1, T426_W);
	PUT_FIFO(T426_o0, 2);
	PUT_FIFO(T426_o1, 3);

	GET_FIFO(T427_i0, 0);
	GET_FIFO(T427_i1, 1);
	Butterfly(T427_i0, T427_i1, &T427_o0, &T427_o1, T427_W);
	PUT_FIFO(T427_o0, 2);
	PUT_FIFO(T427_o1, 3);

	GET_FIFO(T428_i0, 0);
	GET_FIFO(T428_i1, 1);
	Butterfly(T428_i0, T428_i1, &T428_o0, &T428_o1, T428_W);
	PUT_FIFO(T428_o0, 0);
	PUT_FIFO(T428_o1, 1);

	GET_FIFO(T429_i0, 0);
	GET_FIFO(T429_i1, 1);
	Butterfly(T429_i0, T429_i1, &T429_o0, &T429_o1, T429_W);
	PUT_FIFO(T429_o0, 0);
	PUT_FIFO(T429_o1, 1);

	GET_FIFO(T430_i0, 0);
	GET_FIFO(T430_i1, 1);
	Butterfly(T430_i0, T430_i1, &T430_o0, &T430_o1, T430_W);
	PUT_FIFO(T430_o0, 2);
	PUT_FIFO(T430_o1, 3);

	GET_FIFO(T431_i0, 0);
	GET_FIFO(T431_i1, 1);
	Butterfly(T431_i0, T431_i1, &T431_o0, &T431_o1, T431_W);
	PUT_FIFO(T431_o0, 2);
	PUT_FIFO(T431_o1, 3);

	GET_FIFO(T432_i0, 0);
	GET_FIFO(T432_i1, 1);
	Butterfly(T432_i0, T432_i1, &T432_o0, &T432_o1, T432_W);
	PUT_FIFO(T432_o0, 0);
	PUT_FIFO(T432_o1, 1);

	GET_FIFO(T433_i0, 0);
	GET_FIFO(T433_i1, 1);
	Butterfly(T433_i0, T433_i1, &T433_o0, &T433_o1, T433_W);
	PUT_FIFO(T433_o0, 0);
	PUT_FIFO(T433_o1, 1);

	GET_FIFO(T434_i0, 0);
	GET_FIFO(T434_i1, 1);
	Butterfly(T434_i0, T434_i1, &T434_o0, &T434_o1, T434_W);
	PUT_FIFO(T434_o0, 2);
	PUT_FIFO(T434_o1, 3);

	GET_FIFO(T435_i0, 0);
	GET_FIFO(T435_i1, 1);
	Butterfly(T435_i0, T435_i1, &T435_o0, &T435_o1, T435_W);
	PUT_FIFO(T435_o0, 2);
	PUT_FIFO(T435_o1, 3);

	GET_FIFO(T436_i0, 0);
	GET_FIFO(T436_i1, 1);
	Butterfly(T436_i0, T436_i1, &T436_o0, &T436_o1, T436_W);
	PUT_FIFO(T436_o0, 0);
	PUT_FIFO(T436_o1, 1);

	GET_FIFO(T437_i0, 0);
	GET_FIFO(T437_i1, 1);
	Butterfly(T437_i0, T437_i1, &T437_o0, &T437_o1, T437_W);
	PUT_FIFO(T437_o0, 0);
	PUT_FIFO(T437_o1, 1);

	GET_FIFO(T438_i0, 0);
	GET_FIFO(T438_i1, 1);
	Butterfly(T438_i0, T438_i1, &T438_o0, &T438_o1, T438_W);
	PUT_FIFO(T438_o0, 2);
	PUT_FIFO(T438_o1, 3);

	GET_FIFO(T439_i0, 0);
	GET_FIFO(T439_i1, 1);
	Butterfly(T439_i0, T439_i1, &T439_o0, &T439_o1, T439_W);
	PUT_FIFO(T439_o0, 2);
	PUT_FIFO(T439_o1, 3);

	GET_FIFO(T440_i0, 0);
	GET_FIFO(T440_i1, 1);
	Butterfly(T440_i0, T440_i1, &T440_o0, &T440_o1, T440_W);
	PUT_FIFO(T440_o0, 0);
	PUT_FIFO(T440_o1, 1);

	GET_FIFO(T441_i0, 0);
	GET_FIFO(T441_i1, 1);
	Butterfly(T441_i0, T441_i1, &T441_o0, &T441_o1, T441_W);
	PUT_FIFO(T441_o0, 0);
	PUT_FIFO(T441_o1, 1);

	GET_FIFO(T442_i0, 0);
	GET_FIFO(T442_i1, 1);
	Butterfly(T442_i0, T442_i1, &T442_o0, &T442_o1, T442_W);
	PUT_FIFO(T442_o0, 2);
	PUT_FIFO(T442_o1, 3);

	GET_FIFO(T443_i0, 0);
	GET_FIFO(T443_i1, 1);
	Butterfly(T443_i0, T443_i1, &T443_o0, &T443_o1, T443_W);
	PUT_FIFO(T443_o0, 2);
	PUT_FIFO(T443_o1, 3);

	GET_FIFO(T444_i0, 0);
	GET_FIFO(T444_i1, 1);
	Butterfly(T444_i0, T444_i1, &T444_o0, &T444_o1, T444_W);
	PUT_FIFO(T444_o0, 0);
	PUT_FIFO(T444_o1, 1);

	GET_FIFO(T445_i0, 0);
	GET_FIFO(T445_i1, 1);
	Butterfly(T445_i0, T445_i1, &T445_o0, &T445_o1, T445_W);
	PUT_FIFO(T445_o0, 0);
	PUT_FIFO(T445_o1, 1);

	GET_FIFO(T446_i0, 0);
	GET_FIFO(T446_i1, 1);
	Butterfly(T446_i0, T446_i1, &T446_o0, &T446_o1, T446_W);
	PUT_FIFO(T446_o0, 2);
	PUT_FIFO(T446_o1, 3);

	GET_FIFO(T447_i0, 0);
	GET_FIFO(T447_i1, 1);
	Butterfly(T447_i0, T447_i1, &T447_o0, &T447_o1, T447_W);
	PUT_FIFO(T447_o0, 2);
	PUT_FIFO(T447_o1, 3);

	GET_FIFO(T448_i0, 0);
	GET_FIFO(T448_i1, 1);
	Butterfly(T448_i0, T448_i1, &T448_o0, &T448_o1, T448_W);
	PUT_FIFO(T448_o0, 0);
	PUT_FIFO(T448_o1, 1);

	GET_FIFO(T449_i0, 0);
	GET_FIFO(T449_i1, 1);
	Butterfly(T449_i0, T449_i1, &T449_o0, &T449_o1, T449_W);
	PUT_FIFO(T449_o0, 0);
	PUT_FIFO(T449_o1, 1);

	GET_FIFO(T450_i0, 0);
	GET_FIFO(T450_i1, 1);
	Butterfly(T450_i0, T450_i1, &T450_o0, &T450_o1, T450_W);
	PUT_FIFO(T450_o0, 2);
	PUT_FIFO(T450_o1, 3);

	GET_FIFO(T451_i0, 0);
	GET_FIFO(T451_i1, 1);
	Butterfly(T451_i0, T451_i1, &T451_o0, &T451_o1, T451_W);
	PUT_FIFO(T451_o0, 2);
	PUT_FIFO(T451_o1, 3);

	GET_FIFO(T452_i0, 0);
	GET_FIFO(T452_i1, 1);
	Butterfly(T452_i0, T452_i1, &T452_o0, &T452_o1, T452_W);
	PUT_FIFO(T452_o0, 0);
	PUT_FIFO(T452_o1, 1);

	GET_FIFO(T453_i0, 0);
	GET_FIFO(T453_i1, 1);
	Butterfly(T453_i0, T453_i1, &T453_o0, &T453_o1, T453_W);
	PUT_FIFO(T453_o0, 0);
	PUT_FIFO(T453_o1, 1);

	GET_FIFO(T454_i0, 0);
	GET_FIFO(T454_i1, 1);
	Butterfly(T454_i0, T454_i1, &T454_o0, &T454_o1, T454_W);
	PUT_FIFO(T454_o0, 2);
	PUT_FIFO(T454_o1, 3);

	GET_FIFO(T455_i0, 0);
	GET_FIFO(T455_i1, 1);
	Butterfly(T455_i0, T455_i1, &T455_o0, &T455_o1, T455_W);
	PUT_FIFO(T455_o0, 2);
	PUT_FIFO(T455_o1, 3);

	GET_FIFO(T456_i0, 0);
	GET_FIFO(T456_i1, 1);
	Butterfly(T456_i0, T456_i1, &T456_o0, &T456_o1, T456_W);
	PUT_FIFO(T456_o0, 0);
	PUT_FIFO(T456_o1, 1);

	GET_FIFO(T457_i0, 0);
	GET_FIFO(T457_i1, 1);
	Butterfly(T457_i0, T457_i1, &T457_o0, &T457_o1, T457_W);
	PUT_FIFO(T457_o0, 0);
	PUT_FIFO(T457_o1, 1);

	GET_FIFO(T458_i0, 0);
	GET_FIFO(T458_i1, 1);
	Butterfly(T458_i0, T458_i1, &T458_o0, &T458_o1, T458_W);
	PUT_FIFO(T458_o0, 2);
	PUT_FIFO(T458_o1, 3);

	GET_FIFO(T459_i0, 0);
	GET_FIFO(T459_i1, 1);
	Butterfly(T459_i0, T459_i1, &T459_o0, &T459_o1, T459_W);
	PUT_FIFO(T459_o0, 2);
	PUT_FIFO(T459_o1, 3);

	GET_FIFO(T460_i0, 0);
	GET_FIFO(T460_i1, 1);
	Butterfly(T460_i0, T460_i1, &T460_o0, &T460_o1, T460_W);
	PUT_FIFO(T460_o0, 0);
	PUT_FIFO(T460_o1, 1);

	GET_FIFO(T461_i0, 0);
	GET_FIFO(T461_i1, 1);
	Butterfly(T461_i0, T461_i1, &T461_o0, &T461_o1, T461_W);
	PUT_FIFO(T461_o0, 0);
	PUT_FIFO(T461_o1, 1);

	GET_FIFO(T462_i0, 0);
	GET_FIFO(T462_i1, 1);
	Butterfly(T462_i0, T462_i1, &T462_o0, &T462_o1, T462_W);
	PUT_FIFO(T462_o0, 2);
	PUT_FIFO(T462_o1, 3);

	GET_FIFO(T463_i0, 0);
	GET_FIFO(T463_i1, 1);
	Butterfly(T463_i0, T463_i1, &T463_o0, &T463_o1, T463_W);
	PUT_FIFO(T463_o0, 2);
	PUT_FIFO(T463_o1, 3);

	GET_FIFO(T464_i0, 0);
	GET_FIFO(T464_i1, 1);
	Butterfly(T464_i0, T464_i1, &T464_o0, &T464_o1, T464_W);
	PUT_FIFO(T464_o0, 0);
	PUT_FIFO(T464_o1, 1);

	GET_FIFO(T465_i0, 0);
	GET_FIFO(T465_i1, 1);
	Butterfly(T465_i0, T465_i1, &T465_o0, &T465_o1, T465_W);
	PUT_FIFO(T465_o0, 0);
	PUT_FIFO(T465_o1, 1);

	GET_FIFO(T466_i0, 0);
	GET_FIFO(T466_i1, 1);
	Butterfly(T466_i0, T466_i1, &T466_o0, &T466_o1, T466_W);
	PUT_FIFO(T466_o0, 2);
	PUT_FIFO(T466_o1, 3);

	GET_FIFO(T467_i0, 0);
	GET_FIFO(T467_i1, 1);
	Butterfly(T467_i0, T467_i1, &T467_o0, &T467_o1, T467_W);
	PUT_FIFO(T467_o0, 2);
	PUT_FIFO(T467_o1, 3);

	GET_FIFO(T468_i0, 0);
	GET_FIFO(T468_i1, 1);
	Butterfly(T468_i0, T468_i1, &T468_o0, &T468_o1, T468_W);
	PUT_FIFO(T468_o0, 0);
	PUT_FIFO(T468_o1, 1);

	GET_FIFO(T469_i0, 0);
	GET_FIFO(T469_i1, 1);
	Butterfly(T469_i0, T469_i1, &T469_o0, &T469_o1, T469_W);
	PUT_FIFO(T469_o0, 0);
	PUT_FIFO(T469_o1, 1);

	GET_FIFO(T470_i0, 0);
	GET_FIFO(T470_i1, 1);
	Butterfly(T470_i0, T470_i1, &T470_o0, &T470_o1, T470_W);
	PUT_FIFO(T470_o0, 2);
	PUT_FIFO(T470_o1, 3);

	GET_FIFO(T471_i0, 0);
	GET_FIFO(T471_i1, 1);
	Butterfly(T471_i0, T471_i1, &T471_o0, &T471_o1, T471_W);
	PUT_FIFO(T471_o0, 2);
	PUT_FIFO(T471_o1, 3);

	GET_FIFO(T472_i0, 0);
	GET_FIFO(T472_i1, 1);
	Butterfly(T472_i0, T472_i1, &T472_o0, &T472_o1, T472_W);
	PUT_FIFO(T472_o0, 0);
	PUT_FIFO(T472_o1, 1);

	GET_FIFO(T473_i0, 0);
	GET_FIFO(T473_i1, 1);
	Butterfly(T473_i0, T473_i1, &T473_o0, &T473_o1, T473_W);
	PUT_FIFO(T473_o0, 0);
	PUT_FIFO(T473_o1, 1);

	GET_FIFO(T474_i0, 0);
	GET_FIFO(T474_i1, 1);
	Butterfly(T474_i0, T474_i1, &T474_o0, &T474_o1, T474_W);
	PUT_FIFO(T474_o0, 2);
	PUT_FIFO(T474_o1, 3);

	GET_FIFO(T475_i0, 0);
	GET_FIFO(T475_i1, 1);
	Butterfly(T475_i0, T475_i1, &T475_o0, &T475_o1, T475_W);
	PUT_FIFO(T475_o0, 2);
	PUT_FIFO(T475_o1, 3);

	GET_FIFO(T476_i0, 0);
	GET_FIFO(T476_i1, 1);
	Butterfly(T476_i0, T476_i1, &T476_o0, &T476_o1, T476_W);
	PUT_FIFO(T476_o0, 0);
	PUT_FIFO(T476_o1, 1);

	GET_FIFO(T477_i0, 0);
	GET_FIFO(T477_i1, 1);
	Butterfly(T477_i0, T477_i1, &T477_o0, &T477_o1, T477_W);
	PUT_FIFO(T477_o0, 0);
	PUT_FIFO(T477_o1, 1);

	GET_FIFO(T478_i0, 0);
	GET_FIFO(T478_i1, 1);
	Butterfly(T478_i0, T478_i1, &T478_o0, &T478_o1, T478_W);
	PUT_FIFO(T478_o0, 2);
	PUT_FIFO(T478_o1, 3);

	GET_FIFO(T479_i0, 0);
	GET_FIFO(T479_i1, 1);
	Butterfly(T479_i0, T479_i1, &T479_o0, &T479_o1, T479_W);
	PUT_FIFO(T479_o0, 2);
	PUT_FIFO(T479_o1, 3);

	GET_FIFO(T480_i0, 0);
	GET_FIFO(T480_i1, 1);
	Butterfly(T480_i0, T480_i1, &T480_o0, &T480_o1, T480_W);
	PUT_FIFO(T480_o0, 0);
	PUT_FIFO(T480_o1, 1);

	GET_FIFO(T481_i0, 0);
	GET_FIFO(T481_i1, 1);
	Butterfly(T481_i0, T481_i1, &T481_o0, &T481_o1, T481_W);
	PUT_FIFO(T481_o0, 0);
	PUT_FIFO(T481_o1, 1);

	GET_FIFO(T482_i0, 0);
	GET_FIFO(T482_i1, 1);
	Butterfly(T482_i0, T482_i1, &T482_o0, &T482_o1, T482_W);
	PUT_FIFO(T482_o0, 2);
	PUT_FIFO(T482_o1, 3);

	GET_FIFO(T483_i0, 0);
	GET_FIFO(T483_i1, 1);
	Butterfly(T483_i0, T483_i1, &T483_o0, &T483_o1, T483_W);
	PUT_FIFO(T483_o0, 2);
	PUT_FIFO(T483_o1, 3);

	GET_FIFO(T484_i0, 0);
	GET_FIFO(T484_i1, 1);
	Butterfly(T484_i0, T484_i1, &T484_o0, &T484_o1, T484_W);
	PUT_FIFO(T484_o0, 0);
	PUT_FIFO(T484_o1, 1);

	GET_FIFO(T485_i0, 0);
	GET_FIFO(T485_i1, 1);
	Butterfly(T485_i0, T485_i1, &T485_o0, &T485_o1, T485_W);
	PUT_FIFO(T485_o0, 0);
	PUT_FIFO(T485_o1, 1);

	GET_FIFO(T486_i0, 0);
	GET_FIFO(T486_i1, 1);
	Butterfly(T486_i0, T486_i1, &T486_o0, &T486_o1, T486_W);
	PUT_FIFO(T486_o0, 2);
	PUT_FIFO(T486_o1, 3);

	GET_FIFO(T487_i0, 0);
	GET_FIFO(T487_i1, 1);
	Butterfly(T487_i0, T487_i1, &T487_o0, &T487_o1, T487_W);
	PUT_FIFO(T487_o0, 2);
	PUT_FIFO(T487_o1, 3);

	GET_FIFO(T488_i0, 0);
	GET_FIFO(T488_i1, 1);
	Butterfly(T488_i0, T488_i1, &T488_o0, &T488_o1, T488_W);
	PUT_FIFO(T488_o0, 0);
	PUT_FIFO(T488_o1, 1);

	GET_FIFO(T489_i0, 0);
	GET_FIFO(T489_i1, 1);
	Butterfly(T489_i0, T489_i1, &T489_o0, &T489_o1, T489_W);
	PUT_FIFO(T489_o0, 0);
	PUT_FIFO(T489_o1, 1);

	GET_FIFO(T490_i0, 0);
	GET_FIFO(T490_i1, 1);
	Butterfly(T490_i0, T490_i1, &T490_o0, &T490_o1, T490_W);
	PUT_FIFO(T490_o0, 2);
	PUT_FIFO(T490_o1, 3);

	GET_FIFO(T491_i0, 0);
	GET_FIFO(T491_i1, 1);
	Butterfly(T491_i0, T491_i1, &T491_o0, &T491_o1, T491_W);
	PUT_FIFO(T491_o0, 2);
	PUT_FIFO(T491_o1, 3);

	GET_FIFO(T492_i0, 0);
	GET_FIFO(T492_i1, 1);
	Butterfly(T492_i0, T492_i1, &T492_o0, &T492_o1, T492_W);
	PUT_FIFO(T492_o0, 0);
	PUT_FIFO(T492_o1, 1);

	GET_FIFO(T493_i0, 0);
	GET_FIFO(T493_i1, 1);
	Butterfly(T493_i0, T493_i1, &T493_o0, &T493_o1, T493_W);
	PUT_FIFO(T493_o0, 0);
	PUT_FIFO(T493_o1, 1);

	GET_FIFO(T494_i0, 0);
	GET_FIFO(T494_i1, 1);
	Butterfly(T494_i0, T494_i1, &T494_o0, &T494_o1, T494_W);
	PUT_FIFO(T494_o0, 2);
	PUT_FIFO(T494_o1, 3);

	GET_FIFO(T495_i0, 0);
	GET_FIFO(T495_i1, 1);
	Butterfly(T495_i0, T495_i1, &T495_o0, &T495_o1, T495_W);
	PUT_FIFO(T495_o0, 2);
	PUT_FIFO(T495_o1, 3);

	GET_FIFO(T496_i0, 0);
	GET_FIFO(T496_i1, 1);
	Butterfly(T496_i0, T496_i1, &T496_o0, &T496_o1, T496_W);
	PUT_FIFO(T496_o0, 0);
	PUT_FIFO(T496_o1, 1);

	GET_FIFO(T497_i0, 0);
	GET_FIFO(T497_i1, 1);
	Butterfly(T497_i0, T497_i1, &T497_o0, &T497_o1, T497_W);
	PUT_FIFO(T497_o0, 0);
	PUT_FIFO(T497_o1, 1);

	GET_FIFO(T498_i0, 0);
	GET_FIFO(T498_i1, 1);
	Butterfly(T498_i0, T498_i1, &T498_o0, &T498_o1, T498_W);
	PUT_FIFO(T498_o0, 2);
	PUT_FIFO(T498_o1, 3);

	GET_FIFO(T499_i0, 0);
	GET_FIFO(T499_i1, 1);
	Butterfly(T499_i0, T499_i1, &T499_o0, &T499_o1, T499_W);
	PUT_FIFO(T499_o0, 2);
	PUT_FIFO(T499_o1, 3);

	GET_FIFO(T500_i0, 0);
	GET_FIFO(T500_i1, 1);
	Butterfly(T500_i0, T500_i1, &T500_o0, &T500_o1, T500_W);
	PUT_FIFO(T500_o0, 0);
	PUT_FIFO(T500_o1, 1);

	GET_FIFO(T501_i0, 0);
	GET_FIFO(T501_i1, 1);
	Butterfly(T501_i0, T501_i1, &T501_o0, &T501_o1, T501_W);
	PUT_FIFO(T501_o0, 0);
	PUT_FIFO(T501_o1, 1);

	GET_FIFO(T502_i0, 0);
	GET_FIFO(T502_i1, 1);
	Butterfly(T502_i0, T502_i1, &T502_o0, &T502_o1, T502_W);
	PUT_FIFO(T502_o0, 2);
	PUT_FIFO(T502_o1, 3);

	GET_FIFO(T503_i0, 0);
	GET_FIFO(T503_i1, 1);
	Butterfly(T503_i0, T503_i1, &T503_o0, &T503_o1, T503_W);
	PUT_FIFO(T503_o0, 2);
	PUT_FIFO(T503_o1, 3);

	GET_FIFO(T504_i0, 0);
	GET_FIFO(T504_i1, 1);
	Butterfly(T504_i0, T504_i1, &T504_o0, &T504_o1, T504_W);
	PUT_FIFO(T504_o0, 0);
	PUT_FIFO(T504_o1, 1);

	GET_FIFO(T505_i0, 0);
	GET_FIFO(T505_i1, 1);
	Butterfly(T505_i0, T505_i1, &T505_o0, &T505_o1, T505_W);
	PUT_FIFO(T505_o0, 0);
	PUT_FIFO(T505_o1, 1);

	GET_FIFO(T506_i0, 0);
	GET_FIFO(T506_i1, 1);
	Butterfly(T506_i0, T506_i1, &T506_o0, &T506_o1, T506_W);
	PUT_FIFO(T506_o0, 2);
	PUT_FIFO(T506_o1, 3);

	GET_FIFO(T507_i0, 0);
	GET_FIFO(T507_i1, 1);
	Butterfly(T507_i0, T507_i1, &T507_o0, &T507_o1, T507_W);
	PUT_FIFO(T507_o0, 2);
	PUT_FIFO(T507_o1, 3);

	GET_FIFO(T508_i0, 0);
	GET_FIFO(T508_i1, 1);
	Butterfly(T508_i0, T508_i1, &T508_o0, &T508_o1, T508_W);
	PUT_FIFO(T508_o0, 0);
	PUT_FIFO(T508_o1, 1);

	GET_FIFO(T509_i0, 0);
	GET_FIFO(T509_i1, 1);
	Butterfly(T509_i0, T509_i1, &T509_o0, &T509_o1, T509_W);
	PUT_FIFO(T509_o0, 0);
	PUT_FIFO(T509_o1, 1);

	GET_FIFO(T510_i0, 0);
	GET_FIFO(T510_i1, 1);
	Butterfly(T510_i0, T510_i1, &T510_o0, &T510_o1, T510_W);
	PUT_FIFO(T510_o0, 2);
	PUT_FIFO(T510_o1, 3);

	GET_FIFO(T511_i0, 0);
	GET_FIFO(T511_i1, 1);
	Butterfly(T511_i0, T511_i1, &T511_o0, &T511_o1, T511_W);
	PUT_FIFO(T511_o0, 2);
	PUT_FIFO(T511_o1, 3);
}
