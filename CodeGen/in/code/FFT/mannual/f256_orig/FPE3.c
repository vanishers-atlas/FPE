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
void FPE3PE0() {

  // **** Variable declaration **** //
	int T768_i0;
	int T768_i1;
	int T768_o0;
	int T768_o1;
	int T768_W;

	int T769_i0;
	int T769_i1;
	int T769_o0;
	int T769_o1;
	int T769_W;

	int T770_i0;
	int T770_i1;
	int T770_o0;
	int T770_o1;
	int T770_W;

	int T771_i0;
	int T771_i1;
	int T771_o0;
	int T771_o1;
	int T771_W;

	int T772_i0;
	int T772_i1;
	int T772_o0;
	int T772_o1;
	int T772_W;

	int T773_i0;
	int T773_i1;
	int T773_o0;
	int T773_o1;
	int T773_W;

	int T774_i0;
	int T774_i1;
	int T774_o0;
	int T774_o1;
	int T774_W;

	int T775_i0;
	int T775_i1;
	int T775_o0;
	int T775_o1;
	int T775_W;

	int T776_i0;
	int T776_i1;
	int T776_o0;
	int T776_o1;
	int T776_W;

	int T777_i0;
	int T777_i1;
	int T777_o0;
	int T777_o1;
	int T777_W;

	int T778_i0;
	int T778_i1;
	int T778_o0;
	int T778_o1;
	int T778_W;

	int T779_i0;
	int T779_i1;
	int T779_o0;
	int T779_o1;
	int T779_W;

	int T780_i0;
	int T780_i1;
	int T780_o0;
	int T780_o1;
	int T780_W;

	int T781_i0;
	int T781_i1;
	int T781_o0;
	int T781_o1;
	int T781_W;

	int T782_i0;
	int T782_i1;
	int T782_o0;
	int T782_o1;
	int T782_W;

	int T783_i0;
	int T783_i1;
	int T783_o0;
	int T783_o1;
	int T783_W;

	int T784_i0;
	int T784_i1;
	int T784_o0;
	int T784_o1;
	int T784_W;

	int T785_i0;
	int T785_i1;
	int T785_o0;
	int T785_o1;
	int T785_W;

	int T786_i0;
	int T786_i1;
	int T786_o0;
	int T786_o1;
	int T786_W;

	int T787_i0;
	int T787_i1;
	int T787_o0;
	int T787_o1;
	int T787_W;

	int T788_i0;
	int T788_i1;
	int T788_o0;
	int T788_o1;
	int T788_W;

	int T789_i0;
	int T789_i1;
	int T789_o0;
	int T789_o1;
	int T789_W;

	int T790_i0;
	int T790_i1;
	int T790_o0;
	int T790_o1;
	int T790_W;

	int T791_i0;
	int T791_i1;
	int T791_o0;
	int T791_o1;
	int T791_W;

	int T792_i0;
	int T792_i1;
	int T792_o0;
	int T792_o1;
	int T792_W;

	int T793_i0;
	int T793_i1;
	int T793_o0;
	int T793_o1;
	int T793_W;

	int T794_i0;
	int T794_i1;
	int T794_o0;
	int T794_o1;
	int T794_W;

	int T795_i0;
	int T795_i1;
	int T795_o0;
	int T795_o1;
	int T795_W;

	int T796_i0;
	int T796_i1;
	int T796_o0;
	int T796_o1;
	int T796_W;

	int T797_i0;
	int T797_i1;
	int T797_o0;
	int T797_o1;
	int T797_W;

	int T798_i0;
	int T798_i1;
	int T798_o0;
	int T798_o1;
	int T798_W;

	int T799_i0;
	int T799_i1;
	int T799_o0;
	int T799_o1;
	int T799_W;

	int T800_i0;
	int T800_i1;
	int T800_o0;
	int T800_o1;
	int T800_W;

	int T801_i0;
	int T801_i1;
	int T801_o0;
	int T801_o1;
	int T801_W;

	int T802_i0;
	int T802_i1;
	int T802_o0;
	int T802_o1;
	int T802_W;

	int T803_i0;
	int T803_i1;
	int T803_o0;
	int T803_o1;
	int T803_W;

	int T804_i0;
	int T804_i1;
	int T804_o0;
	int T804_o1;
	int T804_W;

	int T805_i0;
	int T805_i1;
	int T805_o0;
	int T805_o1;
	int T805_W;

	int T806_i0;
	int T806_i1;
	int T806_o0;
	int T806_o1;
	int T806_W;

	int T807_i0;
	int T807_i1;
	int T807_o0;
	int T807_o1;
	int T807_W;

	int T808_i0;
	int T808_i1;
	int T808_o0;
	int T808_o1;
	int T808_W;

	int T809_i0;
	int T809_i1;
	int T809_o0;
	int T809_o1;
	int T809_W;

	int T810_i0;
	int T810_i1;
	int T810_o0;
	int T810_o1;
	int T810_W;

	int T811_i0;
	int T811_i1;
	int T811_o0;
	int T811_o1;
	int T811_W;

	int T812_i0;
	int T812_i1;
	int T812_o0;
	int T812_o1;
	int T812_W;

	int T813_i0;
	int T813_i1;
	int T813_o0;
	int T813_o1;
	int T813_W;

	int T814_i0;
	int T814_i1;
	int T814_o0;
	int T814_o1;
	int T814_W;

	int T815_i0;
	int T815_i1;
	int T815_o0;
	int T815_o1;
	int T815_W;

	int T816_i0;
	int T816_i1;
	int T816_o0;
	int T816_o1;
	int T816_W;

	int T817_i0;
	int T817_i1;
	int T817_o0;
	int T817_o1;
	int T817_W;

	int T818_i0;
	int T818_i1;
	int T818_o0;
	int T818_o1;
	int T818_W;

	int T819_i0;
	int T819_i1;
	int T819_o0;
	int T819_o1;
	int T819_W;

	int T820_i0;
	int T820_i1;
	int T820_o0;
	int T820_o1;
	int T820_W;

	int T821_i0;
	int T821_i1;
	int T821_o0;
	int T821_o1;
	int T821_W;

	int T822_i0;
	int T822_i1;
	int T822_o0;
	int T822_o1;
	int T822_W;

	int T823_i0;
	int T823_i1;
	int T823_o0;
	int T823_o1;
	int T823_W;

	int T824_i0;
	int T824_i1;
	int T824_o0;
	int T824_o1;
	int T824_W;

	int T825_i0;
	int T825_i1;
	int T825_o0;
	int T825_o1;
	int T825_W;

	int T826_i0;
	int T826_i1;
	int T826_o0;
	int T826_o1;
	int T826_W;

	int T827_i0;
	int T827_i1;
	int T827_o0;
	int T827_o1;
	int T827_W;

	int T828_i0;
	int T828_i1;
	int T828_o0;
	int T828_o1;
	int T828_W;

	int T829_i0;
	int T829_i1;
	int T829_o0;
	int T829_o1;
	int T829_W;

	int T830_i0;
	int T830_i1;
	int T830_o0;
	int T830_o1;
	int T830_W;

	int T831_i0;
	int T831_i1;
	int T831_o0;
	int T831_o1;
	int T831_W;

	int T832_i0;
	int T832_i1;
	int T832_o0;
	int T832_o1;
	int T832_W;

	int T833_i0;
	int T833_i1;
	int T833_o0;
	int T833_o1;
	int T833_W;

	int T834_i0;
	int T834_i1;
	int T834_o0;
	int T834_o1;
	int T834_W;

	int T835_i0;
	int T835_i1;
	int T835_o0;
	int T835_o1;
	int T835_W;

	int T836_i0;
	int T836_i1;
	int T836_o0;
	int T836_o1;
	int T836_W;

	int T837_i0;
	int T837_i1;
	int T837_o0;
	int T837_o1;
	int T837_W;

	int T838_i0;
	int T838_i1;
	int T838_o0;
	int T838_o1;
	int T838_W;

	int T839_i0;
	int T839_i1;
	int T839_o0;
	int T839_o1;
	int T839_W;

	int T840_i0;
	int T840_i1;
	int T840_o0;
	int T840_o1;
	int T840_W;

	int T841_i0;
	int T841_i1;
	int T841_o0;
	int T841_o1;
	int T841_W;

	int T842_i0;
	int T842_i1;
	int T842_o0;
	int T842_o1;
	int T842_W;

	int T843_i0;
	int T843_i1;
	int T843_o0;
	int T843_o1;
	int T843_W;

	int T844_i0;
	int T844_i1;
	int T844_o0;
	int T844_o1;
	int T844_W;

	int T845_i0;
	int T845_i1;
	int T845_o0;
	int T845_o1;
	int T845_W;

	int T846_i0;
	int T846_i1;
	int T846_o0;
	int T846_o1;
	int T846_W;

	int T847_i0;
	int T847_i1;
	int T847_o0;
	int T847_o1;
	int T847_W;

	int T848_i0;
	int T848_i1;
	int T848_o0;
	int T848_o1;
	int T848_W;

	int T849_i0;
	int T849_i1;
	int T849_o0;
	int T849_o1;
	int T849_W;

	int T850_i0;
	int T850_i1;
	int T850_o0;
	int T850_o1;
	int T850_W;

	int T851_i0;
	int T851_i1;
	int T851_o0;
	int T851_o1;
	int T851_W;

	int T852_i0;
	int T852_i1;
	int T852_o0;
	int T852_o1;
	int T852_W;

	int T853_i0;
	int T853_i1;
	int T853_o0;
	int T853_o1;
	int T853_W;

	int T854_i0;
	int T854_i1;
	int T854_o0;
	int T854_o1;
	int T854_W;

	int T855_i0;
	int T855_i1;
	int T855_o0;
	int T855_o1;
	int T855_W;

	int T856_i0;
	int T856_i1;
	int T856_o0;
	int T856_o1;
	int T856_W;

	int T857_i0;
	int T857_i1;
	int T857_o0;
	int T857_o1;
	int T857_W;

	int T858_i0;
	int T858_i1;
	int T858_o0;
	int T858_o1;
	int T858_W;

	int T859_i0;
	int T859_i1;
	int T859_o0;
	int T859_o1;
	int T859_W;

	int T860_i0;
	int T860_i1;
	int T860_o0;
	int T860_o1;
	int T860_W;

	int T861_i0;
	int T861_i1;
	int T861_o0;
	int T861_o1;
	int T861_W;

	int T862_i0;
	int T862_i1;
	int T862_o0;
	int T862_o1;
	int T862_W;

	int T863_i0;
	int T863_i1;
	int T863_o0;
	int T863_o1;
	int T863_W;

	int T864_i0;
	int T864_i1;
	int T864_o0;
	int T864_o1;
	int T864_W;

	int T865_i0;
	int T865_i1;
	int T865_o0;
	int T865_o1;
	int T865_W;

	int T866_i0;
	int T866_i1;
	int T866_o0;
	int T866_o1;
	int T866_W;

	int T867_i0;
	int T867_i1;
	int T867_o0;
	int T867_o1;
	int T867_W;

	int T868_i0;
	int T868_i1;
	int T868_o0;
	int T868_o1;
	int T868_W;

	int T869_i0;
	int T869_i1;
	int T869_o0;
	int T869_o1;
	int T869_W;

	int T870_i0;
	int T870_i1;
	int T870_o0;
	int T870_o1;
	int T870_W;

	int T871_i0;
	int T871_i1;
	int T871_o0;
	int T871_o1;
	int T871_W;

	int T872_i0;
	int T872_i1;
	int T872_o0;
	int T872_o1;
	int T872_W;

	int T873_i0;
	int T873_i1;
	int T873_o0;
	int T873_o1;
	int T873_W;

	int T874_i0;
	int T874_i1;
	int T874_o0;
	int T874_o1;
	int T874_W;

	int T875_i0;
	int T875_i1;
	int T875_o0;
	int T875_o1;
	int T875_W;

	int T876_i0;
	int T876_i1;
	int T876_o0;
	int T876_o1;
	int T876_W;

	int T877_i0;
	int T877_i1;
	int T877_o0;
	int T877_o1;
	int T877_W;

	int T878_i0;
	int T878_i1;
	int T878_o0;
	int T878_o1;
	int T878_W;

	int T879_i0;
	int T879_i1;
	int T879_o0;
	int T879_o1;
	int T879_W;

	int T880_i0;
	int T880_i1;
	int T880_o0;
	int T880_o1;
	int T880_W;

	int T881_i0;
	int T881_i1;
	int T881_o0;
	int T881_o1;
	int T881_W;

	int T882_i0;
	int T882_i1;
	int T882_o0;
	int T882_o1;
	int T882_W;

	int T883_i0;
	int T883_i1;
	int T883_o0;
	int T883_o1;
	int T883_W;

	int T884_i0;
	int T884_i1;
	int T884_o0;
	int T884_o1;
	int T884_W;

	int T885_i0;
	int T885_i1;
	int T885_o0;
	int T885_o1;
	int T885_W;

	int T886_i0;
	int T886_i1;
	int T886_o0;
	int T886_o1;
	int T886_W;

	int T887_i0;
	int T887_i1;
	int T887_o0;
	int T887_o1;
	int T887_W;

	int T888_i0;
	int T888_i1;
	int T888_o0;
	int T888_o1;
	int T888_W;

	int T889_i0;
	int T889_i1;
	int T889_o0;
	int T889_o1;
	int T889_W;

	int T890_i0;
	int T890_i1;
	int T890_o0;
	int T890_o1;
	int T890_W;

	int T891_i0;
	int T891_i1;
	int T891_o0;
	int T891_o1;
	int T891_W;

	int T892_i0;
	int T892_i1;
	int T892_o0;
	int T892_o1;
	int T892_W;

	int T893_i0;
	int T893_i1;
	int T893_o0;
	int T893_o1;
	int T893_W;

	int T894_i0;
	int T894_i1;
	int T894_o0;
	int T894_o1;
	int T894_W;

	int T895_i0;
	int T895_i1;
	int T895_o0;
	int T895_o1;
	int T895_W;

	int T896_i0;
	int T896_i1;
	int T896_o0;
	int T896_o1;
	int T896_W;

	int T897_i0;
	int T897_i1;
	int T897_o0;
	int T897_o1;
	int T897_W;

	int T898_i0;
	int T898_i1;
	int T898_o0;
	int T898_o1;
	int T898_W;

	int T899_i0;
	int T899_i1;
	int T899_o0;
	int T899_o1;
	int T899_W;

	int T900_i0;
	int T900_i1;
	int T900_o0;
	int T900_o1;
	int T900_W;

	int T901_i0;
	int T901_i1;
	int T901_o0;
	int T901_o1;
	int T901_W;

	int T902_i0;
	int T902_i1;
	int T902_o0;
	int T902_o1;
	int T902_W;

	int T903_i0;
	int T903_i1;
	int T903_o0;
	int T903_o1;
	int T903_W;

	int T904_i0;
	int T904_i1;
	int T904_o0;
	int T904_o1;
	int T904_W;

	int T905_i0;
	int T905_i1;
	int T905_o0;
	int T905_o1;
	int T905_W;

	int T906_i0;
	int T906_i1;
	int T906_o0;
	int T906_o1;
	int T906_W;

	int T907_i0;
	int T907_i1;
	int T907_o0;
	int T907_o1;
	int T907_W;

	int T908_i0;
	int T908_i1;
	int T908_o0;
	int T908_o1;
	int T908_W;

	int T909_i0;
	int T909_i1;
	int T909_o0;
	int T909_o1;
	int T909_W;

	int T910_i0;
	int T910_i1;
	int T910_o0;
	int T910_o1;
	int T910_W;

	int T911_i0;
	int T911_i1;
	int T911_o0;
	int T911_o1;
	int T911_W;

	int T912_i0;
	int T912_i1;
	int T912_o0;
	int T912_o1;
	int T912_W;

	int T913_i0;
	int T913_i1;
	int T913_o0;
	int T913_o1;
	int T913_W;

	int T914_i0;
	int T914_i1;
	int T914_o0;
	int T914_o1;
	int T914_W;

	int T915_i0;
	int T915_i1;
	int T915_o0;
	int T915_o1;
	int T915_W;

	int T916_i0;
	int T916_i1;
	int T916_o0;
	int T916_o1;
	int T916_W;

	int T917_i0;
	int T917_i1;
	int T917_o0;
	int T917_o1;
	int T917_W;

	int T918_i0;
	int T918_i1;
	int T918_o0;
	int T918_o1;
	int T918_W;

	int T919_i0;
	int T919_i1;
	int T919_o0;
	int T919_o1;
	int T919_W;

	int T920_i0;
	int T920_i1;
	int T920_o0;
	int T920_o1;
	int T920_W;

	int T921_i0;
	int T921_i1;
	int T921_o0;
	int T921_o1;
	int T921_W;

	int T922_i0;
	int T922_i1;
	int T922_o0;
	int T922_o1;
	int T922_W;

	int T923_i0;
	int T923_i1;
	int T923_o0;
	int T923_o1;
	int T923_W;

	int T924_i0;
	int T924_i1;
	int T924_o0;
	int T924_o1;
	int T924_W;

	int T925_i0;
	int T925_i1;
	int T925_o0;
	int T925_o1;
	int T925_W;

	int T926_i0;
	int T926_i1;
	int T926_o0;
	int T926_o1;
	int T926_W;

	int T927_i0;
	int T927_i1;
	int T927_o0;
	int T927_o1;
	int T927_W;

	int T928_i0;
	int T928_i1;
	int T928_o0;
	int T928_o1;
	int T928_W;

	int T929_i0;
	int T929_i1;
	int T929_o0;
	int T929_o1;
	int T929_W;

	int T930_i0;
	int T930_i1;
	int T930_o0;
	int T930_o1;
	int T930_W;

	int T931_i0;
	int T931_i1;
	int T931_o0;
	int T931_o1;
	int T931_W;

	int T932_i0;
	int T932_i1;
	int T932_o0;
	int T932_o1;
	int T932_W;

	int T933_i0;
	int T933_i1;
	int T933_o0;
	int T933_o1;
	int T933_W;

	int T934_i0;
	int T934_i1;
	int T934_o0;
	int T934_o1;
	int T934_W;

	int T935_i0;
	int T935_i1;
	int T935_o0;
	int T935_o1;
	int T935_W;

	int T936_i0;
	int T936_i1;
	int T936_o0;
	int T936_o1;
	int T936_W;

	int T937_i0;
	int T937_i1;
	int T937_o0;
	int T937_o1;
	int T937_W;

	int T938_i0;
	int T938_i1;
	int T938_o0;
	int T938_o1;
	int T938_W;

	int T939_i0;
	int T939_i1;
	int T939_o0;
	int T939_o1;
	int T939_W;

	int T940_i0;
	int T940_i1;
	int T940_o0;
	int T940_o1;
	int T940_W;

	int T941_i0;
	int T941_i1;
	int T941_o0;
	int T941_o1;
	int T941_W;

	int T942_i0;
	int T942_i1;
	int T942_o0;
	int T942_o1;
	int T942_W;

	int T943_i0;
	int T943_i1;
	int T943_o0;
	int T943_o1;
	int T943_W;

	int T944_i0;
	int T944_i1;
	int T944_o0;
	int T944_o1;
	int T944_W;

	int T945_i0;
	int T945_i1;
	int T945_o0;
	int T945_o1;
	int T945_W;

	int T946_i0;
	int T946_i1;
	int T946_o0;
	int T946_o1;
	int T946_W;

	int T947_i0;
	int T947_i1;
	int T947_o0;
	int T947_o1;
	int T947_W;

	int T948_i0;
	int T948_i1;
	int T948_o0;
	int T948_o1;
	int T948_W;

	int T949_i0;
	int T949_i1;
	int T949_o0;
	int T949_o1;
	int T949_W;

	int T950_i0;
	int T950_i1;
	int T950_o0;
	int T950_o1;
	int T950_W;

	int T951_i0;
	int T951_i1;
	int T951_o0;
	int T951_o1;
	int T951_W;

	int T952_i0;
	int T952_i1;
	int T952_o0;
	int T952_o1;
	int T952_W;

	int T953_i0;
	int T953_i1;
	int T953_o0;
	int T953_o1;
	int T953_W;

	int T954_i0;
	int T954_i1;
	int T954_o0;
	int T954_o1;
	int T954_W;

	int T955_i0;
	int T955_i1;
	int T955_o0;
	int T955_o1;
	int T955_W;

	int T956_i0;
	int T956_i1;
	int T956_o0;
	int T956_o1;
	int T956_W;

	int T957_i0;
	int T957_i1;
	int T957_o0;
	int T957_o1;
	int T957_W;

	int T958_i0;
	int T958_i1;
	int T958_o0;
	int T958_o1;
	int T958_W;

	int T959_i0;
	int T959_i1;
	int T959_o0;
	int T959_o1;
	int T959_W;

	int T960_i0;
	int T960_i1;
	int T960_o0;
	int T960_o1;
	int T960_W;

	int T961_i0;
	int T961_i1;
	int T961_o0;
	int T961_o1;
	int T961_W;

	int T962_i0;
	int T962_i1;
	int T962_o0;
	int T962_o1;
	int T962_W;

	int T963_i0;
	int T963_i1;
	int T963_o0;
	int T963_o1;
	int T963_W;

	int T964_i0;
	int T964_i1;
	int T964_o0;
	int T964_o1;
	int T964_W;

	int T965_i0;
	int T965_i1;
	int T965_o0;
	int T965_o1;
	int T965_W;

	int T966_i0;
	int T966_i1;
	int T966_o0;
	int T966_o1;
	int T966_W;

	int T967_i0;
	int T967_i1;
	int T967_o0;
	int T967_o1;
	int T967_W;

	int T968_i0;
	int T968_i1;
	int T968_o0;
	int T968_o1;
	int T968_W;

	int T969_i0;
	int T969_i1;
	int T969_o0;
	int T969_o1;
	int T969_W;

	int T970_i0;
	int T970_i1;
	int T970_o0;
	int T970_o1;
	int T970_W;

	int T971_i0;
	int T971_i1;
	int T971_o0;
	int T971_o1;
	int T971_W;

	int T972_i0;
	int T972_i1;
	int T972_o0;
	int T972_o1;
	int T972_W;

	int T973_i0;
	int T973_i1;
	int T973_o0;
	int T973_o1;
	int T973_W;

	int T974_i0;
	int T974_i1;
	int T974_o0;
	int T974_o1;
	int T974_W;

	int T975_i0;
	int T975_i1;
	int T975_o0;
	int T975_o1;
	int T975_W;

	int T976_i0;
	int T976_i1;
	int T976_o0;
	int T976_o1;
	int T976_W;

	int T977_i0;
	int T977_i1;
	int T977_o0;
	int T977_o1;
	int T977_W;

	int T978_i0;
	int T978_i1;
	int T978_o0;
	int T978_o1;
	int T978_W;

	int T979_i0;
	int T979_i1;
	int T979_o0;
	int T979_o1;
	int T979_W;

	int T980_i0;
	int T980_i1;
	int T980_o0;
	int T980_o1;
	int T980_W;

	int T981_i0;
	int T981_i1;
	int T981_o0;
	int T981_o1;
	int T981_W;

	int T982_i0;
	int T982_i1;
	int T982_o0;
	int T982_o1;
	int T982_W;

	int T983_i0;
	int T983_i1;
	int T983_o0;
	int T983_o1;
	int T983_W;

	int T984_i0;
	int T984_i1;
	int T984_o0;
	int T984_o1;
	int T984_W;

	int T985_i0;
	int T985_i1;
	int T985_o0;
	int T985_o1;
	int T985_W;

	int T986_i0;
	int T986_i1;
	int T986_o0;
	int T986_o1;
	int T986_W;

	int T987_i0;
	int T987_i1;
	int T987_o0;
	int T987_o1;
	int T987_W;

	int T988_i0;
	int T988_i1;
	int T988_o0;
	int T988_o1;
	int T988_W;

	int T989_i0;
	int T989_i1;
	int T989_o0;
	int T989_o1;
	int T989_W;

	int T990_i0;
	int T990_i1;
	int T990_o0;
	int T990_o1;
	int T990_W;

	int T991_i0;
	int T991_i1;
	int T991_o0;
	int T991_o1;
	int T991_W;

	int T992_i0;
	int T992_i1;
	int T992_o0;
	int T992_o1;
	int T992_W;

	int T993_i0;
	int T993_i1;
	int T993_o0;
	int T993_o1;
	int T993_W;

	int T994_i0;
	int T994_i1;
	int T994_o0;
	int T994_o1;
	int T994_W;

	int T995_i0;
	int T995_i1;
	int T995_o0;
	int T995_o1;
	int T995_W;

	int T996_i0;
	int T996_i1;
	int T996_o0;
	int T996_o1;
	int T996_W;

	int T997_i0;
	int T997_i1;
	int T997_o0;
	int T997_o1;
	int T997_W;

	int T998_i0;
	int T998_i1;
	int T998_o0;
	int T998_o1;
	int T998_W;

	int T999_i0;
	int T999_i1;
	int T999_o0;
	int T999_o1;
	int T999_W;

	int T1000_i0;
	int T1000_i1;
	int T1000_o0;
	int T1000_o1;
	int T1000_W;

	int T1001_i0;
	int T1001_i1;
	int T1001_o0;
	int T1001_o1;
	int T1001_W;

	int T1002_i0;
	int T1002_i1;
	int T1002_o0;
	int T1002_o1;
	int T1002_W;

	int T1003_i0;
	int T1003_i1;
	int T1003_o0;
	int T1003_o1;
	int T1003_W;

	int T1004_i0;
	int T1004_i1;
	int T1004_o0;
	int T1004_o1;
	int T1004_W;

	int T1005_i0;
	int T1005_i1;
	int T1005_o0;
	int T1005_o1;
	int T1005_W;

	int T1006_i0;
	int T1006_i1;
	int T1006_o0;
	int T1006_o1;
	int T1006_W;

	int T1007_i0;
	int T1007_i1;
	int T1007_o0;
	int T1007_o1;
	int T1007_W;

	int T1008_i0;
	int T1008_i1;
	int T1008_o0;
	int T1008_o1;
	int T1008_W;

	int T1009_i0;
	int T1009_i1;
	int T1009_o0;
	int T1009_o1;
	int T1009_W;

	int T1010_i0;
	int T1010_i1;
	int T1010_o0;
	int T1010_o1;
	int T1010_W;

	int T1011_i0;
	int T1011_i1;
	int T1011_o0;
	int T1011_o1;
	int T1011_W;

	int T1012_i0;
	int T1012_i1;
	int T1012_o0;
	int T1012_o1;
	int T1012_W;

	int T1013_i0;
	int T1013_i1;
	int T1013_o0;
	int T1013_o1;
	int T1013_W;

	int T1014_i0;
	int T1014_i1;
	int T1014_o0;
	int T1014_o1;
	int T1014_W;

	int T1015_i0;
	int T1015_i1;
	int T1015_o0;
	int T1015_o1;
	int T1015_W;

	int T1016_i0;
	int T1016_i1;
	int T1016_o0;
	int T1016_o1;
	int T1016_W;

	int T1017_i0;
	int T1017_i1;
	int T1017_o0;
	int T1017_o1;
	int T1017_W;

	int T1018_i0;
	int T1018_i1;
	int T1018_o0;
	int T1018_o1;
	int T1018_W;

	int T1019_i0;
	int T1019_i1;
	int T1019_o0;
	int T1019_o1;
	int T1019_W;

	int T1020_i0;
	int T1020_i1;
	int T1020_o0;
	int T1020_o1;
	int T1020_W;

	int T1021_i0;
	int T1021_i1;
	int T1021_o0;
	int T1021_o1;
	int T1021_W;

	int T1022_i0;
	int T1022_i1;
	int T1022_o0;
	int T1022_o1;
	int T1022_W;

	int T1023_i0;
	int T1023_i1;
	int T1023_o0;
	int T1023_o1;
	int T1023_W;


  // **** Parameter initialisation **** //
T768_W = 16384;
T769_W = -410895583;
T770_W = -759222975;
T771_W = -992012162;
T772_W = -1073741824;
T773_W = -992024702;
T774_W = -759246145;
T775_W = -410925857;
T776_W = 16384;
T777_W = -410895583;
T778_W = -759222975;
T779_W = -992012162;
T780_W = -1073741824;
T781_W = -992024702;
T782_W = -759246145;
T783_W = -410925857;
T784_W = 16384;
T785_W = -410895583;
T786_W = -759222975;
T787_W = -992012162;
T788_W = -1073741824;
T789_W = -992024702;
T790_W = -759246145;
T791_W = -410925857;
T792_W = 16384;
T793_W = -410895583;
T794_W = -759222975;
T795_W = -992012162;
T796_W = -1073741824;
T797_W = -992024702;
T798_W = -759246145;
T799_W = -410925857;
T800_W = 16384;
T801_W = -410895583;
T802_W = -759222975;
T803_W = -992012162;
T804_W = -1073741824;
T805_W = -992024702;
T806_W = -759246145;
T807_W = -410925857;
T808_W = 16384;
T809_W = -410895583;
T810_W = -759222975;
T811_W = -992012162;
T812_W = -1073741824;
T813_W = -992024702;
T814_W = -759246145;
T815_W = -410925857;
T816_W = 16384;
T817_W = -410895583;
T818_W = -759222975;
T819_W = -992012162;
T820_W = -1073741824;
T821_W = -992024702;
T822_W = -759246145;
T823_W = -410925857;
T824_W = 16384;
T825_W = -410895583;
T826_W = -759222975;
T827_W = -992012162;
T828_W = -1073741824;
T829_W = -992024702;
T830_W = -759246145;
T831_W = -410925857;
T832_W = 16384;
T833_W = -410895583;
T834_W = -759222975;
T835_W = -992012162;
T836_W = -1073741824;
T837_W = -992024702;
T838_W = -759246145;
T839_W = -410925857;
T840_W = 16384;
T841_W = -410895583;
T842_W = -759222975;
T843_W = -992012162;
T844_W = -1073741824;
T845_W = -992024702;
T846_W = -759246145;
T847_W = -410925857;
T848_W = 16384;
T849_W = -410895583;
T850_W = -759222975;
T851_W = -992012162;
T852_W = -1073741824;
T853_W = -992024702;
T854_W = -759246145;
T855_W = -410925857;
T856_W = 16384;
T857_W = -410895583;
T858_W = -759222975;
T859_W = -992012162;
T860_W = -1073741824;
T861_W = -992024702;
T862_W = -759246145;
T863_W = -410925857;
T864_W = 16384;
T865_W = -410895583;
T866_W = -759222975;
T867_W = -992012162;
T868_W = -1073741824;
T869_W = -992024702;
T870_W = -759246145;
T871_W = -410925857;
T872_W = 16384;
T873_W = -410895583;
T874_W = -759222975;
T875_W = -992012162;
T876_W = -1073741824;
T877_W = -992024702;
T878_W = -759246145;
T879_W = -410925857;
T880_W = 16384;
T881_W = -410895583;
T882_W = -759222975;
T883_W = -992012162;
T884_W = -1073741824;
T885_W = -992024702;
T886_W = -759246145;
T887_W = -410925857;
T888_W = 16384;
T889_W = -410895583;
T890_W = -759222975;
T891_W = -992012162;
T892_W = -1073741824;
T893_W = -992024702;
T894_W = -759246145;
T895_W = -410925857;
T896_W = 16384;
T897_W = -410895583;
T898_W = -759222975;
T899_W = -992012162;
T900_W = -1073741824;
T901_W = -992024702;
T902_W = -759246145;
T903_W = -410925857;
T904_W = 16384;
T905_W = -410895583;
T906_W = -759222975;
T907_W = -992012162;
T908_W = -1073741824;
T909_W = -992024702;
T910_W = -759246145;
T911_W = -410925857;
T912_W = 16384;
T913_W = -410895583;
T914_W = -759222975;
T915_W = -992012162;
T916_W = -1073741824;
T917_W = -992024702;
T918_W = -759246145;
T919_W = -410925857;
T920_W = 16384;
T921_W = -410895583;
T922_W = -759222975;
T923_W = -992012162;
T924_W = -1073741824;
T925_W = -992024702;
T926_W = -759246145;
T927_W = -410925857;
T928_W = 16384;
T929_W = -410895583;
T930_W = -759222975;
T931_W = -992012162;
T932_W = -1073741824;
T933_W = -992024702;
T934_W = -759246145;
T935_W = -410925857;
T936_W = 16384;
T937_W = -410895583;
T938_W = -759222975;
T939_W = -992012162;
T940_W = -1073741824;
T941_W = -992024702;
T942_W = -759246145;
T943_W = -410925857;
T944_W = 16384;
T945_W = -410895583;
T946_W = -759222975;
T947_W = -992012162;
T948_W = -1073741824;
T949_W = -992024702;
T950_W = -759246145;
T951_W = -410925857;
T952_W = 16384;
T953_W = -410895583;
T954_W = -759222975;
T955_W = -992012162;
T956_W = -1073741824;
T957_W = -992024702;
T958_W = -759246145;
T959_W = -410925857;
T960_W = 16384;
T961_W = -410895583;
T962_W = -759222975;
T963_W = -992012162;
T964_W = -1073741824;
T965_W = -992024702;
T966_W = -759246145;
T967_W = -410925857;
T968_W = 16384;
T969_W = -410895583;
T970_W = -759222975;
T971_W = -992012162;
T972_W = -1073741824;
T973_W = -992024702;
T974_W = -759246145;
T975_W = -410925857;
T976_W = 16384;
T977_W = -410895583;
T978_W = -759222975;
T979_W = -992012162;
T980_W = -1073741824;
T981_W = -992024702;
T982_W = -759246145;
T983_W = -410925857;
T984_W = 16384;
T985_W = -410895583;
T986_W = -759222975;
T987_W = -992012162;
T988_W = -1073741824;
T989_W = -992024702;
T990_W = -759246145;
T991_W = -410925857;
T992_W = 16384;
T993_W = -410895583;
T994_W = -759222975;
T995_W = -992012162;
T996_W = -1073741824;
T997_W = -992024702;
T998_W = -759246145;
T999_W = -410925857;
T1000_W = 16384;
T1001_W = -410895583;
T1002_W = -759222975;
T1003_W = -992012162;
T1004_W = -1073741824;
T1005_W = -992024702;
T1006_W = -759246145;
T1007_W = -410925857;
T1008_W = 16384;
T1009_W = -410895583;
T1010_W = -759222975;
T1011_W = -992012162;
T1012_W = -1073741824;
T1013_W = -992024702;
T1014_W = -759246145;
T1015_W = -410925857;
T1016_W = 16384;
T1017_W = -410895583;
T1018_W = -759222975;
T1019_W = -992012162;
T1020_W = -1073741824;
T1021_W = -992024702;
T1022_W = -759246145;
T1023_W = -410925857;

  // **** Code body **** //

	GET_FIFO(T768_i0, 0);
	GET_FIFO(T768_i1, 2);
	Butterfly(T768_i0, T768_i1, &T768_o0, &T768_o1, T768_W);
	PUT_FIFO(T768_o0, 0);
	PUT_FIFO(T768_o1, 1);

	GET_FIFO(T769_i0, 0);
	GET_FIFO(T769_i1, 2);
	Butterfly(T769_i0, T769_i1, &T769_o0, &T769_o1, T769_W);
	PUT_FIFO(T769_o0, 0);
	PUT_FIFO(T769_o1, 1);

	GET_FIFO(T770_i0, 0);
	GET_FIFO(T770_i1, 2);
	Butterfly(T770_i0, T770_i1, &T770_o0, &T770_o1, T770_W);
	PUT_FIFO(T770_o0, 0);
	PUT_FIFO(T770_o1, 1);

	GET_FIFO(T771_i0, 0);
	GET_FIFO(T771_i1, 2);
	Butterfly(T771_i0, T771_i1, &T771_o0, &T771_o1, T771_W);
	PUT_FIFO(T771_o0, 0);
	PUT_FIFO(T771_o1, 1);

	GET_FIFO(T772_i0, 1);
	GET_FIFO(T772_i1, 3);
	Butterfly(T772_i0, T772_i1, &T772_o0, &T772_o1, T772_W);
	PUT_FIFO(T772_o0, 0);
	PUT_FIFO(T772_o1, 1);

	GET_FIFO(T773_i0, 1);
	GET_FIFO(T773_i1, 3);
	Butterfly(T773_i0, T773_i1, &T773_o0, &T773_o1, T773_W);
	PUT_FIFO(T773_o0, 0);
	PUT_FIFO(T773_o1, 1);

	GET_FIFO(T774_i0, 1);
	GET_FIFO(T774_i1, 3);
	Butterfly(T774_i0, T774_i1, &T774_o0, &T774_o1, T774_W);
	PUT_FIFO(T774_o0, 0);
	PUT_FIFO(T774_o1, 1);

	GET_FIFO(T775_i0, 1);
	GET_FIFO(T775_i1, 3);
	Butterfly(T775_i0, T775_i1, &T775_o0, &T775_o1, T775_W);
	PUT_FIFO(T775_o0, 0);
	PUT_FIFO(T775_o1, 1);

	GET_FIFO(T776_i0, 0);
	GET_FIFO(T776_i1, 2);
	Butterfly(T776_i0, T776_i1, &T776_o0, &T776_o1, T776_W);
	PUT_FIFO(T776_o0, 2);
	PUT_FIFO(T776_o1, 3);

	GET_FIFO(T777_i0, 0);
	GET_FIFO(T777_i1, 2);
	Butterfly(T777_i0, T777_i1, &T777_o0, &T777_o1, T777_W);
	PUT_FIFO(T777_o0, 2);
	PUT_FIFO(T777_o1, 3);

	GET_FIFO(T778_i0, 0);
	GET_FIFO(T778_i1, 2);
	Butterfly(T778_i0, T778_i1, &T778_o0, &T778_o1, T778_W);
	PUT_FIFO(T778_o0, 2);
	PUT_FIFO(T778_o1, 3);

	GET_FIFO(T779_i0, 0);
	GET_FIFO(T779_i1, 2);
	Butterfly(T779_i0, T779_i1, &T779_o0, &T779_o1, T779_W);
	PUT_FIFO(T779_o0, 2);
	PUT_FIFO(T779_o1, 3);

	GET_FIFO(T780_i0, 1);
	GET_FIFO(T780_i1, 3);
	Butterfly(T780_i0, T780_i1, &T780_o0, &T780_o1, T780_W);
	PUT_FIFO(T780_o0, 2);
	PUT_FIFO(T780_o1, 3);

	GET_FIFO(T781_i0, 1);
	GET_FIFO(T781_i1, 3);
	Butterfly(T781_i0, T781_i1, &T781_o0, &T781_o1, T781_W);
	PUT_FIFO(T781_o0, 2);
	PUT_FIFO(T781_o1, 3);

	GET_FIFO(T782_i0, 1);
	GET_FIFO(T782_i1, 3);
	Butterfly(T782_i0, T782_i1, &T782_o0, &T782_o1, T782_W);
	PUT_FIFO(T782_o0, 2);
	PUT_FIFO(T782_o1, 3);

	GET_FIFO(T783_i0, 1);
	GET_FIFO(T783_i1, 3);
	Butterfly(T783_i0, T783_i1, &T783_o0, &T783_o1, T783_W);
	PUT_FIFO(T783_o0, 2);
	PUT_FIFO(T783_o1, 3);

	GET_FIFO(T784_i0, 0);
	GET_FIFO(T784_i1, 2);
	Butterfly(T784_i0, T784_i1, &T784_o0, &T784_o1, T784_W);
	PUT_FIFO(T784_o0, 0);
	PUT_FIFO(T784_o1, 1);

	GET_FIFO(T785_i0, 0);
	GET_FIFO(T785_i1, 2);
	Butterfly(T785_i0, T785_i1, &T785_o0, &T785_o1, T785_W);
	PUT_FIFO(T785_o0, 0);
	PUT_FIFO(T785_o1, 1);

	GET_FIFO(T786_i0, 0);
	GET_FIFO(T786_i1, 2);
	Butterfly(T786_i0, T786_i1, &T786_o0, &T786_o1, T786_W);
	PUT_FIFO(T786_o0, 0);
	PUT_FIFO(T786_o1, 1);

	GET_FIFO(T787_i0, 0);
	GET_FIFO(T787_i1, 2);
	Butterfly(T787_i0, T787_i1, &T787_o0, &T787_o1, T787_W);
	PUT_FIFO(T787_o0, 0);
	PUT_FIFO(T787_o1, 1);

	GET_FIFO(T788_i0, 1);
	GET_FIFO(T788_i1, 3);
	Butterfly(T788_i0, T788_i1, &T788_o0, &T788_o1, T788_W);
	PUT_FIFO(T788_o0, 0);
	PUT_FIFO(T788_o1, 1);

	GET_FIFO(T789_i0, 1);
	GET_FIFO(T789_i1, 3);
	Butterfly(T789_i0, T789_i1, &T789_o0, &T789_o1, T789_W);
	PUT_FIFO(T789_o0, 0);
	PUT_FIFO(T789_o1, 1);

	GET_FIFO(T790_i0, 1);
	GET_FIFO(T790_i1, 3);
	Butterfly(T790_i0, T790_i1, &T790_o0, &T790_o1, T790_W);
	PUT_FIFO(T790_o0, 0);
	PUT_FIFO(T790_o1, 1);

	GET_FIFO(T791_i0, 1);
	GET_FIFO(T791_i1, 3);
	Butterfly(T791_i0, T791_i1, &T791_o0, &T791_o1, T791_W);
	PUT_FIFO(T791_o0, 0);
	PUT_FIFO(T791_o1, 1);

	GET_FIFO(T792_i0, 0);
	GET_FIFO(T792_i1, 2);
	Butterfly(T792_i0, T792_i1, &T792_o0, &T792_o1, T792_W);
	PUT_FIFO(T792_o0, 2);
	PUT_FIFO(T792_o1, 3);

	GET_FIFO(T793_i0, 0);
	GET_FIFO(T793_i1, 2);
	Butterfly(T793_i0, T793_i1, &T793_o0, &T793_o1, T793_W);
	PUT_FIFO(T793_o0, 2);
	PUT_FIFO(T793_o1, 3);

	GET_FIFO(T794_i0, 0);
	GET_FIFO(T794_i1, 2);
	Butterfly(T794_i0, T794_i1, &T794_o0, &T794_o1, T794_W);
	PUT_FIFO(T794_o0, 2);
	PUT_FIFO(T794_o1, 3);

	GET_FIFO(T795_i0, 0);
	GET_FIFO(T795_i1, 2);
	Butterfly(T795_i0, T795_i1, &T795_o0, &T795_o1, T795_W);
	PUT_FIFO(T795_o0, 2);
	PUT_FIFO(T795_o1, 3);

	GET_FIFO(T796_i0, 1);
	GET_FIFO(T796_i1, 3);
	Butterfly(T796_i0, T796_i1, &T796_o0, &T796_o1, T796_W);
	PUT_FIFO(T796_o0, 2);
	PUT_FIFO(T796_o1, 3);

	GET_FIFO(T797_i0, 1);
	GET_FIFO(T797_i1, 3);
	Butterfly(T797_i0, T797_i1, &T797_o0, &T797_o1, T797_W);
	PUT_FIFO(T797_o0, 2);
	PUT_FIFO(T797_o1, 3);

	GET_FIFO(T798_i0, 1);
	GET_FIFO(T798_i1, 3);
	Butterfly(T798_i0, T798_i1, &T798_o0, &T798_o1, T798_W);
	PUT_FIFO(T798_o0, 2);
	PUT_FIFO(T798_o1, 3);

	GET_FIFO(T799_i0, 1);
	GET_FIFO(T799_i1, 3);
	Butterfly(T799_i0, T799_i1, &T799_o0, &T799_o1, T799_W);
	PUT_FIFO(T799_o0, 2);
	PUT_FIFO(T799_o1, 3);

	GET_FIFO(T800_i0, 0);
	GET_FIFO(T800_i1, 2);
	Butterfly(T800_i0, T800_i1, &T800_o0, &T800_o1, T800_W);
	PUT_FIFO(T800_o0, 0);
	PUT_FIFO(T800_o1, 1);

	GET_FIFO(T801_i0, 0);
	GET_FIFO(T801_i1, 2);
	Butterfly(T801_i0, T801_i1, &T801_o0, &T801_o1, T801_W);
	PUT_FIFO(T801_o0, 0);
	PUT_FIFO(T801_o1, 1);

	GET_FIFO(T802_i0, 0);
	GET_FIFO(T802_i1, 2);
	Butterfly(T802_i0, T802_i1, &T802_o0, &T802_o1, T802_W);
	PUT_FIFO(T802_o0, 0);
	PUT_FIFO(T802_o1, 1);

	GET_FIFO(T803_i0, 0);
	GET_FIFO(T803_i1, 2);
	Butterfly(T803_i0, T803_i1, &T803_o0, &T803_o1, T803_W);
	PUT_FIFO(T803_o0, 0);
	PUT_FIFO(T803_o1, 1);

	GET_FIFO(T804_i0, 1);
	GET_FIFO(T804_i1, 3);
	Butterfly(T804_i0, T804_i1, &T804_o0, &T804_o1, T804_W);
	PUT_FIFO(T804_o0, 0);
	PUT_FIFO(T804_o1, 1);

	GET_FIFO(T805_i0, 1);
	GET_FIFO(T805_i1, 3);
	Butterfly(T805_i0, T805_i1, &T805_o0, &T805_o1, T805_W);
	PUT_FIFO(T805_o0, 0);
	PUT_FIFO(T805_o1, 1);

	GET_FIFO(T806_i0, 1);
	GET_FIFO(T806_i1, 3);
	Butterfly(T806_i0, T806_i1, &T806_o0, &T806_o1, T806_W);
	PUT_FIFO(T806_o0, 0);
	PUT_FIFO(T806_o1, 1);

	GET_FIFO(T807_i0, 1);
	GET_FIFO(T807_i1, 3);
	Butterfly(T807_i0, T807_i1, &T807_o0, &T807_o1, T807_W);
	PUT_FIFO(T807_o0, 0);
	PUT_FIFO(T807_o1, 1);

	GET_FIFO(T808_i0, 0);
	GET_FIFO(T808_i1, 2);
	Butterfly(T808_i0, T808_i1, &T808_o0, &T808_o1, T808_W);
	PUT_FIFO(T808_o0, 2);
	PUT_FIFO(T808_o1, 3);

	GET_FIFO(T809_i0, 0);
	GET_FIFO(T809_i1, 2);
	Butterfly(T809_i0, T809_i1, &T809_o0, &T809_o1, T809_W);
	PUT_FIFO(T809_o0, 2);
	PUT_FIFO(T809_o1, 3);

	GET_FIFO(T810_i0, 0);
	GET_FIFO(T810_i1, 2);
	Butterfly(T810_i0, T810_i1, &T810_o0, &T810_o1, T810_W);
	PUT_FIFO(T810_o0, 2);
	PUT_FIFO(T810_o1, 3);

	GET_FIFO(T811_i0, 0);
	GET_FIFO(T811_i1, 2);
	Butterfly(T811_i0, T811_i1, &T811_o0, &T811_o1, T811_W);
	PUT_FIFO(T811_o0, 2);
	PUT_FIFO(T811_o1, 3);

	GET_FIFO(T812_i0, 1);
	GET_FIFO(T812_i1, 3);
	Butterfly(T812_i0, T812_i1, &T812_o0, &T812_o1, T812_W);
	PUT_FIFO(T812_o0, 2);
	PUT_FIFO(T812_o1, 3);

	GET_FIFO(T813_i0, 1);
	GET_FIFO(T813_i1, 3);
	Butterfly(T813_i0, T813_i1, &T813_o0, &T813_o1, T813_W);
	PUT_FIFO(T813_o0, 2);
	PUT_FIFO(T813_o1, 3);

	GET_FIFO(T814_i0, 1);
	GET_FIFO(T814_i1, 3);
	Butterfly(T814_i0, T814_i1, &T814_o0, &T814_o1, T814_W);
	PUT_FIFO(T814_o0, 2);
	PUT_FIFO(T814_o1, 3);

	GET_FIFO(T815_i0, 1);
	GET_FIFO(T815_i1, 3);
	Butterfly(T815_i0, T815_i1, &T815_o0, &T815_o1, T815_W);
	PUT_FIFO(T815_o0, 2);
	PUT_FIFO(T815_o1, 3);

	GET_FIFO(T816_i0, 0);
	GET_FIFO(T816_i1, 2);
	Butterfly(T816_i0, T816_i1, &T816_o0, &T816_o1, T816_W);
	PUT_FIFO(T816_o0, 0);
	PUT_FIFO(T816_o1, 1);

	GET_FIFO(T817_i0, 0);
	GET_FIFO(T817_i1, 2);
	Butterfly(T817_i0, T817_i1, &T817_o0, &T817_o1, T817_W);
	PUT_FIFO(T817_o0, 0);
	PUT_FIFO(T817_o1, 1);

	GET_FIFO(T818_i0, 0);
	GET_FIFO(T818_i1, 2);
	Butterfly(T818_i0, T818_i1, &T818_o0, &T818_o1, T818_W);
	PUT_FIFO(T818_o0, 0);
	PUT_FIFO(T818_o1, 1);

	GET_FIFO(T819_i0, 0);
	GET_FIFO(T819_i1, 2);
	Butterfly(T819_i0, T819_i1, &T819_o0, &T819_o1, T819_W);
	PUT_FIFO(T819_o0, 0);
	PUT_FIFO(T819_o1, 1);

	GET_FIFO(T820_i0, 1);
	GET_FIFO(T820_i1, 3);
	Butterfly(T820_i0, T820_i1, &T820_o0, &T820_o1, T820_W);
	PUT_FIFO(T820_o0, 0);
	PUT_FIFO(T820_o1, 1);

	GET_FIFO(T821_i0, 1);
	GET_FIFO(T821_i1, 3);
	Butterfly(T821_i0, T821_i1, &T821_o0, &T821_o1, T821_W);
	PUT_FIFO(T821_o0, 0);
	PUT_FIFO(T821_o1, 1);

	GET_FIFO(T822_i0, 1);
	GET_FIFO(T822_i1, 3);
	Butterfly(T822_i0, T822_i1, &T822_o0, &T822_o1, T822_W);
	PUT_FIFO(T822_o0, 0);
	PUT_FIFO(T822_o1, 1);

	GET_FIFO(T823_i0, 1);
	GET_FIFO(T823_i1, 3);
	Butterfly(T823_i0, T823_i1, &T823_o0, &T823_o1, T823_W);
	PUT_FIFO(T823_o0, 0);
	PUT_FIFO(T823_o1, 1);

	GET_FIFO(T824_i0, 0);
	GET_FIFO(T824_i1, 2);
	Butterfly(T824_i0, T824_i1, &T824_o0, &T824_o1, T824_W);
	PUT_FIFO(T824_o0, 2);
	PUT_FIFO(T824_o1, 3);

	GET_FIFO(T825_i0, 0);
	GET_FIFO(T825_i1, 2);
	Butterfly(T825_i0, T825_i1, &T825_o0, &T825_o1, T825_W);
	PUT_FIFO(T825_o0, 2);
	PUT_FIFO(T825_o1, 3);

	GET_FIFO(T826_i0, 0);
	GET_FIFO(T826_i1, 2);
	Butterfly(T826_i0, T826_i1, &T826_o0, &T826_o1, T826_W);
	PUT_FIFO(T826_o0, 2);
	PUT_FIFO(T826_o1, 3);

	GET_FIFO(T827_i0, 0);
	GET_FIFO(T827_i1, 2);
	Butterfly(T827_i0, T827_i1, &T827_o0, &T827_o1, T827_W);
	PUT_FIFO(T827_o0, 2);
	PUT_FIFO(T827_o1, 3);

	GET_FIFO(T828_i0, 1);
	GET_FIFO(T828_i1, 3);
	Butterfly(T828_i0, T828_i1, &T828_o0, &T828_o1, T828_W);
	PUT_FIFO(T828_o0, 2);
	PUT_FIFO(T828_o1, 3);

	GET_FIFO(T829_i0, 1);
	GET_FIFO(T829_i1, 3);
	Butterfly(T829_i0, T829_i1, &T829_o0, &T829_o1, T829_W);
	PUT_FIFO(T829_o0, 2);
	PUT_FIFO(T829_o1, 3);

	GET_FIFO(T830_i0, 1);
	GET_FIFO(T830_i1, 3);
	Butterfly(T830_i0, T830_i1, &T830_o0, &T830_o1, T830_W);
	PUT_FIFO(T830_o0, 2);
	PUT_FIFO(T830_o1, 3);

	GET_FIFO(T831_i0, 1);
	GET_FIFO(T831_i1, 3);
	Butterfly(T831_i0, T831_i1, &T831_o0, &T831_o1, T831_W);
	PUT_FIFO(T831_o0, 2);
	PUT_FIFO(T831_o1, 3);

	GET_FIFO(T832_i0, 0);
	GET_FIFO(T832_i1, 2);
	Butterfly(T832_i0, T832_i1, &T832_o0, &T832_o1, T832_W);
	PUT_FIFO(T832_o0, 0);
	PUT_FIFO(T832_o1, 1);

	GET_FIFO(T833_i0, 0);
	GET_FIFO(T833_i1, 2);
	Butterfly(T833_i0, T833_i1, &T833_o0, &T833_o1, T833_W);
	PUT_FIFO(T833_o0, 0);
	PUT_FIFO(T833_o1, 1);

	GET_FIFO(T834_i0, 0);
	GET_FIFO(T834_i1, 2);
	Butterfly(T834_i0, T834_i1, &T834_o0, &T834_o1, T834_W);
	PUT_FIFO(T834_o0, 0);
	PUT_FIFO(T834_o1, 1);

	GET_FIFO(T835_i0, 0);
	GET_FIFO(T835_i1, 2);
	Butterfly(T835_i0, T835_i1, &T835_o0, &T835_o1, T835_W);
	PUT_FIFO(T835_o0, 0);
	PUT_FIFO(T835_o1, 1);

	GET_FIFO(T836_i0, 1);
	GET_FIFO(T836_i1, 3);
	Butterfly(T836_i0, T836_i1, &T836_o0, &T836_o1, T836_W);
	PUT_FIFO(T836_o0, 0);
	PUT_FIFO(T836_o1, 1);

	GET_FIFO(T837_i0, 1);
	GET_FIFO(T837_i1, 3);
	Butterfly(T837_i0, T837_i1, &T837_o0, &T837_o1, T837_W);
	PUT_FIFO(T837_o0, 0);
	PUT_FIFO(T837_o1, 1);

	GET_FIFO(T838_i0, 1);
	GET_FIFO(T838_i1, 3);
	Butterfly(T838_i0, T838_i1, &T838_o0, &T838_o1, T838_W);
	PUT_FIFO(T838_o0, 0);
	PUT_FIFO(T838_o1, 1);

	GET_FIFO(T839_i0, 1);
	GET_FIFO(T839_i1, 3);
	Butterfly(T839_i0, T839_i1, &T839_o0, &T839_o1, T839_W);
	PUT_FIFO(T839_o0, 0);
	PUT_FIFO(T839_o1, 1);

	GET_FIFO(T840_i0, 0);
	GET_FIFO(T840_i1, 2);
	Butterfly(T840_i0, T840_i1, &T840_o0, &T840_o1, T840_W);
	PUT_FIFO(T840_o0, 2);
	PUT_FIFO(T840_o1, 3);

	GET_FIFO(T841_i0, 0);
	GET_FIFO(T841_i1, 2);
	Butterfly(T841_i0, T841_i1, &T841_o0, &T841_o1, T841_W);
	PUT_FIFO(T841_o0, 2);
	PUT_FIFO(T841_o1, 3);

	GET_FIFO(T842_i0, 0);
	GET_FIFO(T842_i1, 2);
	Butterfly(T842_i0, T842_i1, &T842_o0, &T842_o1, T842_W);
	PUT_FIFO(T842_o0, 2);
	PUT_FIFO(T842_o1, 3);

	GET_FIFO(T843_i0, 0);
	GET_FIFO(T843_i1, 2);
	Butterfly(T843_i0, T843_i1, &T843_o0, &T843_o1, T843_W);
	PUT_FIFO(T843_o0, 2);
	PUT_FIFO(T843_o1, 3);

	GET_FIFO(T844_i0, 1);
	GET_FIFO(T844_i1, 3);
	Butterfly(T844_i0, T844_i1, &T844_o0, &T844_o1, T844_W);
	PUT_FIFO(T844_o0, 2);
	PUT_FIFO(T844_o1, 3);

	GET_FIFO(T845_i0, 1);
	GET_FIFO(T845_i1, 3);
	Butterfly(T845_i0, T845_i1, &T845_o0, &T845_o1, T845_W);
	PUT_FIFO(T845_o0, 2);
	PUT_FIFO(T845_o1, 3);

	GET_FIFO(T846_i0, 1);
	GET_FIFO(T846_i1, 3);
	Butterfly(T846_i0, T846_i1, &T846_o0, &T846_o1, T846_W);
	PUT_FIFO(T846_o0, 2);
	PUT_FIFO(T846_o1, 3);

	GET_FIFO(T847_i0, 1);
	GET_FIFO(T847_i1, 3);
	Butterfly(T847_i0, T847_i1, &T847_o0, &T847_o1, T847_W);
	PUT_FIFO(T847_o0, 2);
	PUT_FIFO(T847_o1, 3);

	GET_FIFO(T848_i0, 0);
	GET_FIFO(T848_i1, 2);
	Butterfly(T848_i0, T848_i1, &T848_o0, &T848_o1, T848_W);
	PUT_FIFO(T848_o0, 0);
	PUT_FIFO(T848_o1, 1);

	GET_FIFO(T849_i0, 0);
	GET_FIFO(T849_i1, 2);
	Butterfly(T849_i0, T849_i1, &T849_o0, &T849_o1, T849_W);
	PUT_FIFO(T849_o0, 0);
	PUT_FIFO(T849_o1, 1);

	GET_FIFO(T850_i0, 0);
	GET_FIFO(T850_i1, 2);
	Butterfly(T850_i0, T850_i1, &T850_o0, &T850_o1, T850_W);
	PUT_FIFO(T850_o0, 0);
	PUT_FIFO(T850_o1, 1);

	GET_FIFO(T851_i0, 0);
	GET_FIFO(T851_i1, 2);
	Butterfly(T851_i0, T851_i1, &T851_o0, &T851_o1, T851_W);
	PUT_FIFO(T851_o0, 0);
	PUT_FIFO(T851_o1, 1);

	GET_FIFO(T852_i0, 1);
	GET_FIFO(T852_i1, 3);
	Butterfly(T852_i0, T852_i1, &T852_o0, &T852_o1, T852_W);
	PUT_FIFO(T852_o0, 0);
	PUT_FIFO(T852_o1, 1);

	GET_FIFO(T853_i0, 1);
	GET_FIFO(T853_i1, 3);
	Butterfly(T853_i0, T853_i1, &T853_o0, &T853_o1, T853_W);
	PUT_FIFO(T853_o0, 0);
	PUT_FIFO(T853_o1, 1);

	GET_FIFO(T854_i0, 1);
	GET_FIFO(T854_i1, 3);
	Butterfly(T854_i0, T854_i1, &T854_o0, &T854_o1, T854_W);
	PUT_FIFO(T854_o0, 0);
	PUT_FIFO(T854_o1, 1);

	GET_FIFO(T855_i0, 1);
	GET_FIFO(T855_i1, 3);
	Butterfly(T855_i0, T855_i1, &T855_o0, &T855_o1, T855_W);
	PUT_FIFO(T855_o0, 0);
	PUT_FIFO(T855_o1, 1);

	GET_FIFO(T856_i0, 0);
	GET_FIFO(T856_i1, 2);
	Butterfly(T856_i0, T856_i1, &T856_o0, &T856_o1, T856_W);
	PUT_FIFO(T856_o0, 2);
	PUT_FIFO(T856_o1, 3);

	GET_FIFO(T857_i0, 0);
	GET_FIFO(T857_i1, 2);
	Butterfly(T857_i0, T857_i1, &T857_o0, &T857_o1, T857_W);
	PUT_FIFO(T857_o0, 2);
	PUT_FIFO(T857_o1, 3);

	GET_FIFO(T858_i0, 0);
	GET_FIFO(T858_i1, 2);
	Butterfly(T858_i0, T858_i1, &T858_o0, &T858_o1, T858_W);
	PUT_FIFO(T858_o0, 2);
	PUT_FIFO(T858_o1, 3);

	GET_FIFO(T859_i0, 0);
	GET_FIFO(T859_i1, 2);
	Butterfly(T859_i0, T859_i1, &T859_o0, &T859_o1, T859_W);
	PUT_FIFO(T859_o0, 2);
	PUT_FIFO(T859_o1, 3);

	GET_FIFO(T860_i0, 1);
	GET_FIFO(T860_i1, 3);
	Butterfly(T860_i0, T860_i1, &T860_o0, &T860_o1, T860_W);
	PUT_FIFO(T860_o0, 2);
	PUT_FIFO(T860_o1, 3);

	GET_FIFO(T861_i0, 1);
	GET_FIFO(T861_i1, 3);
	Butterfly(T861_i0, T861_i1, &T861_o0, &T861_o1, T861_W);
	PUT_FIFO(T861_o0, 2);
	PUT_FIFO(T861_o1, 3);

	GET_FIFO(T862_i0, 1);
	GET_FIFO(T862_i1, 3);
	Butterfly(T862_i0, T862_i1, &T862_o0, &T862_o1, T862_W);
	PUT_FIFO(T862_o0, 2);
	PUT_FIFO(T862_o1, 3);

	GET_FIFO(T863_i0, 1);
	GET_FIFO(T863_i1, 3);
	Butterfly(T863_i0, T863_i1, &T863_o0, &T863_o1, T863_W);
	PUT_FIFO(T863_o0, 2);
	PUT_FIFO(T863_o1, 3);

	GET_FIFO(T864_i0, 0);
	GET_FIFO(T864_i1, 2);
	Butterfly(T864_i0, T864_i1, &T864_o0, &T864_o1, T864_W);
	PUT_FIFO(T864_o0, 0);
	PUT_FIFO(T864_o1, 1);

	GET_FIFO(T865_i0, 0);
	GET_FIFO(T865_i1, 2);
	Butterfly(T865_i0, T865_i1, &T865_o0, &T865_o1, T865_W);
	PUT_FIFO(T865_o0, 0);
	PUT_FIFO(T865_o1, 1);

	GET_FIFO(T866_i0, 0);
	GET_FIFO(T866_i1, 2);
	Butterfly(T866_i0, T866_i1, &T866_o0, &T866_o1, T866_W);
	PUT_FIFO(T866_o0, 0);
	PUT_FIFO(T866_o1, 1);

	GET_FIFO(T867_i0, 0);
	GET_FIFO(T867_i1, 2);
	Butterfly(T867_i0, T867_i1, &T867_o0, &T867_o1, T867_W);
	PUT_FIFO(T867_o0, 0);
	PUT_FIFO(T867_o1, 1);

	GET_FIFO(T868_i0, 1);
	GET_FIFO(T868_i1, 3);
	Butterfly(T868_i0, T868_i1, &T868_o0, &T868_o1, T868_W);
	PUT_FIFO(T868_o0, 0);
	PUT_FIFO(T868_o1, 1);

	GET_FIFO(T869_i0, 1);
	GET_FIFO(T869_i1, 3);
	Butterfly(T869_i0, T869_i1, &T869_o0, &T869_o1, T869_W);
	PUT_FIFO(T869_o0, 0);
	PUT_FIFO(T869_o1, 1);

	GET_FIFO(T870_i0, 1);
	GET_FIFO(T870_i1, 3);
	Butterfly(T870_i0, T870_i1, &T870_o0, &T870_o1, T870_W);
	PUT_FIFO(T870_o0, 0);
	PUT_FIFO(T870_o1, 1);

	GET_FIFO(T871_i0, 1);
	GET_FIFO(T871_i1, 3);
	Butterfly(T871_i0, T871_i1, &T871_o0, &T871_o1, T871_W);
	PUT_FIFO(T871_o0, 0);
	PUT_FIFO(T871_o1, 1);

	GET_FIFO(T872_i0, 0);
	GET_FIFO(T872_i1, 2);
	Butterfly(T872_i0, T872_i1, &T872_o0, &T872_o1, T872_W);
	PUT_FIFO(T872_o0, 2);
	PUT_FIFO(T872_o1, 3);

	GET_FIFO(T873_i0, 0);
	GET_FIFO(T873_i1, 2);
	Butterfly(T873_i0, T873_i1, &T873_o0, &T873_o1, T873_W);
	PUT_FIFO(T873_o0, 2);
	PUT_FIFO(T873_o1, 3);

	GET_FIFO(T874_i0, 0);
	GET_FIFO(T874_i1, 2);
	Butterfly(T874_i0, T874_i1, &T874_o0, &T874_o1, T874_W);
	PUT_FIFO(T874_o0, 2);
	PUT_FIFO(T874_o1, 3);

	GET_FIFO(T875_i0, 0);
	GET_FIFO(T875_i1, 2);
	Butterfly(T875_i0, T875_i1, &T875_o0, &T875_o1, T875_W);
	PUT_FIFO(T875_o0, 2);
	PUT_FIFO(T875_o1, 3);

	GET_FIFO(T876_i0, 1);
	GET_FIFO(T876_i1, 3);
	Butterfly(T876_i0, T876_i1, &T876_o0, &T876_o1, T876_W);
	PUT_FIFO(T876_o0, 2);
	PUT_FIFO(T876_o1, 3);

	GET_FIFO(T877_i0, 1);
	GET_FIFO(T877_i1, 3);
	Butterfly(T877_i0, T877_i1, &T877_o0, &T877_o1, T877_W);
	PUT_FIFO(T877_o0, 2);
	PUT_FIFO(T877_o1, 3);

	GET_FIFO(T878_i0, 1);
	GET_FIFO(T878_i1, 3);
	Butterfly(T878_i0, T878_i1, &T878_o0, &T878_o1, T878_W);
	PUT_FIFO(T878_o0, 2);
	PUT_FIFO(T878_o1, 3);

	GET_FIFO(T879_i0, 1);
	GET_FIFO(T879_i1, 3);
	Butterfly(T879_i0, T879_i1, &T879_o0, &T879_o1, T879_W);
	PUT_FIFO(T879_o0, 2);
	PUT_FIFO(T879_o1, 3);

	GET_FIFO(T880_i0, 0);
	GET_FIFO(T880_i1, 2);
	Butterfly(T880_i0, T880_i1, &T880_o0, &T880_o1, T880_W);
	PUT_FIFO(T880_o0, 0);
	PUT_FIFO(T880_o1, 1);

	GET_FIFO(T881_i0, 0);
	GET_FIFO(T881_i1, 2);
	Butterfly(T881_i0, T881_i1, &T881_o0, &T881_o1, T881_W);
	PUT_FIFO(T881_o0, 0);
	PUT_FIFO(T881_o1, 1);

	GET_FIFO(T882_i0, 0);
	GET_FIFO(T882_i1, 2);
	Butterfly(T882_i0, T882_i1, &T882_o0, &T882_o1, T882_W);
	PUT_FIFO(T882_o0, 0);
	PUT_FIFO(T882_o1, 1);

	GET_FIFO(T883_i0, 0);
	GET_FIFO(T883_i1, 2);
	Butterfly(T883_i0, T883_i1, &T883_o0, &T883_o1, T883_W);
	PUT_FIFO(T883_o0, 0);
	PUT_FIFO(T883_o1, 1);

	GET_FIFO(T884_i0, 1);
	GET_FIFO(T884_i1, 3);
	Butterfly(T884_i0, T884_i1, &T884_o0, &T884_o1, T884_W);
	PUT_FIFO(T884_o0, 0);
	PUT_FIFO(T884_o1, 1);

	GET_FIFO(T885_i0, 1);
	GET_FIFO(T885_i1, 3);
	Butterfly(T885_i0, T885_i1, &T885_o0, &T885_o1, T885_W);
	PUT_FIFO(T885_o0, 0);
	PUT_FIFO(T885_o1, 1);

	GET_FIFO(T886_i0, 1);
	GET_FIFO(T886_i1, 3);
	Butterfly(T886_i0, T886_i1, &T886_o0, &T886_o1, T886_W);
	PUT_FIFO(T886_o0, 0);
	PUT_FIFO(T886_o1, 1);

	GET_FIFO(T887_i0, 1);
	GET_FIFO(T887_i1, 3);
	Butterfly(T887_i0, T887_i1, &T887_o0, &T887_o1, T887_W);
	PUT_FIFO(T887_o0, 0);
	PUT_FIFO(T887_o1, 1);

	GET_FIFO(T888_i0, 0);
	GET_FIFO(T888_i1, 2);
	Butterfly(T888_i0, T888_i1, &T888_o0, &T888_o1, T888_W);
	PUT_FIFO(T888_o0, 2);
	PUT_FIFO(T888_o1, 3);

	GET_FIFO(T889_i0, 0);
	GET_FIFO(T889_i1, 2);
	Butterfly(T889_i0, T889_i1, &T889_o0, &T889_o1, T889_W);
	PUT_FIFO(T889_o0, 2);
	PUT_FIFO(T889_o1, 3);

	GET_FIFO(T890_i0, 0);
	GET_FIFO(T890_i1, 2);
	Butterfly(T890_i0, T890_i1, &T890_o0, &T890_o1, T890_W);
	PUT_FIFO(T890_o0, 2);
	PUT_FIFO(T890_o1, 3);

	GET_FIFO(T891_i0, 0);
	GET_FIFO(T891_i1, 2);
	Butterfly(T891_i0, T891_i1, &T891_o0, &T891_o1, T891_W);
	PUT_FIFO(T891_o0, 2);
	PUT_FIFO(T891_o1, 3);

	GET_FIFO(T892_i0, 1);
	GET_FIFO(T892_i1, 3);
	Butterfly(T892_i0, T892_i1, &T892_o0, &T892_o1, T892_W);
	PUT_FIFO(T892_o0, 2);
	PUT_FIFO(T892_o1, 3);

	GET_FIFO(T893_i0, 1);
	GET_FIFO(T893_i1, 3);
	Butterfly(T893_i0, T893_i1, &T893_o0, &T893_o1, T893_W);
	PUT_FIFO(T893_o0, 2);
	PUT_FIFO(T893_o1, 3);

	GET_FIFO(T894_i0, 1);
	GET_FIFO(T894_i1, 3);
	Butterfly(T894_i0, T894_i1, &T894_o0, &T894_o1, T894_W);
	PUT_FIFO(T894_o0, 2);
	PUT_FIFO(T894_o1, 3);

	GET_FIFO(T895_i0, 1);
	GET_FIFO(T895_i1, 3);
	Butterfly(T895_i0, T895_i1, &T895_o0, &T895_o1, T895_W);
	PUT_FIFO(T895_o0, 2);
	PUT_FIFO(T895_o1, 3);

	GET_FIFO(T896_i0, 0);
	GET_FIFO(T896_i1, 2);
	Butterfly(T896_i0, T896_i1, &T896_o0, &T896_o1, T896_W);
	PUT_FIFO(T896_o0, 0);
	PUT_FIFO(T896_o1, 1);

	GET_FIFO(T897_i0, 0);
	GET_FIFO(T897_i1, 2);
	Butterfly(T897_i0, T897_i1, &T897_o0, &T897_o1, T897_W);
	PUT_FIFO(T897_o0, 0);
	PUT_FIFO(T897_o1, 1);

	GET_FIFO(T898_i0, 0);
	GET_FIFO(T898_i1, 2);
	Butterfly(T898_i0, T898_i1, &T898_o0, &T898_o1, T898_W);
	PUT_FIFO(T898_o0, 0);
	PUT_FIFO(T898_o1, 1);

	GET_FIFO(T899_i0, 0);
	GET_FIFO(T899_i1, 2);
	Butterfly(T899_i0, T899_i1, &T899_o0, &T899_o1, T899_W);
	PUT_FIFO(T899_o0, 0);
	PUT_FIFO(T899_o1, 1);

	GET_FIFO(T900_i0, 1);
	GET_FIFO(T900_i1, 3);
	Butterfly(T900_i0, T900_i1, &T900_o0, &T900_o1, T900_W);
	PUT_FIFO(T900_o0, 0);
	PUT_FIFO(T900_o1, 1);

	GET_FIFO(T901_i0, 1);
	GET_FIFO(T901_i1, 3);
	Butterfly(T901_i0, T901_i1, &T901_o0, &T901_o1, T901_W);
	PUT_FIFO(T901_o0, 0);
	PUT_FIFO(T901_o1, 1);

	GET_FIFO(T902_i0, 1);
	GET_FIFO(T902_i1, 3);
	Butterfly(T902_i0, T902_i1, &T902_o0, &T902_o1, T902_W);
	PUT_FIFO(T902_o0, 0);
	PUT_FIFO(T902_o1, 1);

	GET_FIFO(T903_i0, 1);
	GET_FIFO(T903_i1, 3);
	Butterfly(T903_i0, T903_i1, &T903_o0, &T903_o1, T903_W);
	PUT_FIFO(T903_o0, 0);
	PUT_FIFO(T903_o1, 1);

	GET_FIFO(T904_i0, 0);
	GET_FIFO(T904_i1, 2);
	Butterfly(T904_i0, T904_i1, &T904_o0, &T904_o1, T904_W);
	PUT_FIFO(T904_o0, 2);
	PUT_FIFO(T904_o1, 3);

	GET_FIFO(T905_i0, 0);
	GET_FIFO(T905_i1, 2);
	Butterfly(T905_i0, T905_i1, &T905_o0, &T905_o1, T905_W);
	PUT_FIFO(T905_o0, 2);
	PUT_FIFO(T905_o1, 3);

	GET_FIFO(T906_i0, 0);
	GET_FIFO(T906_i1, 2);
	Butterfly(T906_i0, T906_i1, &T906_o0, &T906_o1, T906_W);
	PUT_FIFO(T906_o0, 2);
	PUT_FIFO(T906_o1, 3);

	GET_FIFO(T907_i0, 0);
	GET_FIFO(T907_i1, 2);
	Butterfly(T907_i0, T907_i1, &T907_o0, &T907_o1, T907_W);
	PUT_FIFO(T907_o0, 2);
	PUT_FIFO(T907_o1, 3);

	GET_FIFO(T908_i0, 1);
	GET_FIFO(T908_i1, 3);
	Butterfly(T908_i0, T908_i1, &T908_o0, &T908_o1, T908_W);
	PUT_FIFO(T908_o0, 2);
	PUT_FIFO(T908_o1, 3);

	GET_FIFO(T909_i0, 1);
	GET_FIFO(T909_i1, 3);
	Butterfly(T909_i0, T909_i1, &T909_o0, &T909_o1, T909_W);
	PUT_FIFO(T909_o0, 2);
	PUT_FIFO(T909_o1, 3);

	GET_FIFO(T910_i0, 1);
	GET_FIFO(T910_i1, 3);
	Butterfly(T910_i0, T910_i1, &T910_o0, &T910_o1, T910_W);
	PUT_FIFO(T910_o0, 2);
	PUT_FIFO(T910_o1, 3);

	GET_FIFO(T911_i0, 1);
	GET_FIFO(T911_i1, 3);
	Butterfly(T911_i0, T911_i1, &T911_o0, &T911_o1, T911_W);
	PUT_FIFO(T911_o0, 2);
	PUT_FIFO(T911_o1, 3);

	GET_FIFO(T912_i0, 0);
	GET_FIFO(T912_i1, 2);
	Butterfly(T912_i0, T912_i1, &T912_o0, &T912_o1, T912_W);
	PUT_FIFO(T912_o0, 0);
	PUT_FIFO(T912_o1, 1);

	GET_FIFO(T913_i0, 0);
	GET_FIFO(T913_i1, 2);
	Butterfly(T913_i0, T913_i1, &T913_o0, &T913_o1, T913_W);
	PUT_FIFO(T913_o0, 0);
	PUT_FIFO(T913_o1, 1);

	GET_FIFO(T914_i0, 0);
	GET_FIFO(T914_i1, 2);
	Butterfly(T914_i0, T914_i1, &T914_o0, &T914_o1, T914_W);
	PUT_FIFO(T914_o0, 0);
	PUT_FIFO(T914_o1, 1);

	GET_FIFO(T915_i0, 0);
	GET_FIFO(T915_i1, 2);
	Butterfly(T915_i0, T915_i1, &T915_o0, &T915_o1, T915_W);
	PUT_FIFO(T915_o0, 0);
	PUT_FIFO(T915_o1, 1);

	GET_FIFO(T916_i0, 1);
	GET_FIFO(T916_i1, 3);
	Butterfly(T916_i0, T916_i1, &T916_o0, &T916_o1, T916_W);
	PUT_FIFO(T916_o0, 0);
	PUT_FIFO(T916_o1, 1);

	GET_FIFO(T917_i0, 1);
	GET_FIFO(T917_i1, 3);
	Butterfly(T917_i0, T917_i1, &T917_o0, &T917_o1, T917_W);
	PUT_FIFO(T917_o0, 0);
	PUT_FIFO(T917_o1, 1);

	GET_FIFO(T918_i0, 1);
	GET_FIFO(T918_i1, 3);
	Butterfly(T918_i0, T918_i1, &T918_o0, &T918_o1, T918_W);
	PUT_FIFO(T918_o0, 0);
	PUT_FIFO(T918_o1, 1);

	GET_FIFO(T919_i0, 1);
	GET_FIFO(T919_i1, 3);
	Butterfly(T919_i0, T919_i1, &T919_o0, &T919_o1, T919_W);
	PUT_FIFO(T919_o0, 0);
	PUT_FIFO(T919_o1, 1);

	GET_FIFO(T920_i0, 0);
	GET_FIFO(T920_i1, 2);
	Butterfly(T920_i0, T920_i1, &T920_o0, &T920_o1, T920_W);
	PUT_FIFO(T920_o0, 2);
	PUT_FIFO(T920_o1, 3);

	GET_FIFO(T921_i0, 0);
	GET_FIFO(T921_i1, 2);
	Butterfly(T921_i0, T921_i1, &T921_o0, &T921_o1, T921_W);
	PUT_FIFO(T921_o0, 2);
	PUT_FIFO(T921_o1, 3);

	GET_FIFO(T922_i0, 0);
	GET_FIFO(T922_i1, 2);
	Butterfly(T922_i0, T922_i1, &T922_o0, &T922_o1, T922_W);
	PUT_FIFO(T922_o0, 2);
	PUT_FIFO(T922_o1, 3);

	GET_FIFO(T923_i0, 0);
	GET_FIFO(T923_i1, 2);
	Butterfly(T923_i0, T923_i1, &T923_o0, &T923_o1, T923_W);
	PUT_FIFO(T923_o0, 2);
	PUT_FIFO(T923_o1, 3);

	GET_FIFO(T924_i0, 1);
	GET_FIFO(T924_i1, 3);
	Butterfly(T924_i0, T924_i1, &T924_o0, &T924_o1, T924_W);
	PUT_FIFO(T924_o0, 2);
	PUT_FIFO(T924_o1, 3);

	GET_FIFO(T925_i0, 1);
	GET_FIFO(T925_i1, 3);
	Butterfly(T925_i0, T925_i1, &T925_o0, &T925_o1, T925_W);
	PUT_FIFO(T925_o0, 2);
	PUT_FIFO(T925_o1, 3);

	GET_FIFO(T926_i0, 1);
	GET_FIFO(T926_i1, 3);
	Butterfly(T926_i0, T926_i1, &T926_o0, &T926_o1, T926_W);
	PUT_FIFO(T926_o0, 2);
	PUT_FIFO(T926_o1, 3);

	GET_FIFO(T927_i0, 1);
	GET_FIFO(T927_i1, 3);
	Butterfly(T927_i0, T927_i1, &T927_o0, &T927_o1, T927_W);
	PUT_FIFO(T927_o0, 2);
	PUT_FIFO(T927_o1, 3);

	GET_FIFO(T928_i0, 0);
	GET_FIFO(T928_i1, 2);
	Butterfly(T928_i0, T928_i1, &T928_o0, &T928_o1, T928_W);
	PUT_FIFO(T928_o0, 0);
	PUT_FIFO(T928_o1, 1);

	GET_FIFO(T929_i0, 0);
	GET_FIFO(T929_i1, 2);
	Butterfly(T929_i0, T929_i1, &T929_o0, &T929_o1, T929_W);
	PUT_FIFO(T929_o0, 0);
	PUT_FIFO(T929_o1, 1);

	GET_FIFO(T930_i0, 0);
	GET_FIFO(T930_i1, 2);
	Butterfly(T930_i0, T930_i1, &T930_o0, &T930_o1, T930_W);
	PUT_FIFO(T930_o0, 0);
	PUT_FIFO(T930_o1, 1);

	GET_FIFO(T931_i0, 0);
	GET_FIFO(T931_i1, 2);
	Butterfly(T931_i0, T931_i1, &T931_o0, &T931_o1, T931_W);
	PUT_FIFO(T931_o0, 0);
	PUT_FIFO(T931_o1, 1);

	GET_FIFO(T932_i0, 1);
	GET_FIFO(T932_i1, 3);
	Butterfly(T932_i0, T932_i1, &T932_o0, &T932_o1, T932_W);
	PUT_FIFO(T932_o0, 0);
	PUT_FIFO(T932_o1, 1);

	GET_FIFO(T933_i0, 1);
	GET_FIFO(T933_i1, 3);
	Butterfly(T933_i0, T933_i1, &T933_o0, &T933_o1, T933_W);
	PUT_FIFO(T933_o0, 0);
	PUT_FIFO(T933_o1, 1);

	GET_FIFO(T934_i0, 1);
	GET_FIFO(T934_i1, 3);
	Butterfly(T934_i0, T934_i1, &T934_o0, &T934_o1, T934_W);
	PUT_FIFO(T934_o0, 0);
	PUT_FIFO(T934_o1, 1);

	GET_FIFO(T935_i0, 1);
	GET_FIFO(T935_i1, 3);
	Butterfly(T935_i0, T935_i1, &T935_o0, &T935_o1, T935_W);
	PUT_FIFO(T935_o0, 0);
	PUT_FIFO(T935_o1, 1);

	GET_FIFO(T936_i0, 0);
	GET_FIFO(T936_i1, 2);
	Butterfly(T936_i0, T936_i1, &T936_o0, &T936_o1, T936_W);
	PUT_FIFO(T936_o0, 2);
	PUT_FIFO(T936_o1, 3);

	GET_FIFO(T937_i0, 0);
	GET_FIFO(T937_i1, 2);
	Butterfly(T937_i0, T937_i1, &T937_o0, &T937_o1, T937_W);
	PUT_FIFO(T937_o0, 2);
	PUT_FIFO(T937_o1, 3);

	GET_FIFO(T938_i0, 0);
	GET_FIFO(T938_i1, 2);
	Butterfly(T938_i0, T938_i1, &T938_o0, &T938_o1, T938_W);
	PUT_FIFO(T938_o0, 2);
	PUT_FIFO(T938_o1, 3);

	GET_FIFO(T939_i0, 0);
	GET_FIFO(T939_i1, 2);
	Butterfly(T939_i0, T939_i1, &T939_o0, &T939_o1, T939_W);
	PUT_FIFO(T939_o0, 2);
	PUT_FIFO(T939_o1, 3);

	GET_FIFO(T940_i0, 1);
	GET_FIFO(T940_i1, 3);
	Butterfly(T940_i0, T940_i1, &T940_o0, &T940_o1, T940_W);
	PUT_FIFO(T940_o0, 2);
	PUT_FIFO(T940_o1, 3);

	GET_FIFO(T941_i0, 1);
	GET_FIFO(T941_i1, 3);
	Butterfly(T941_i0, T941_i1, &T941_o0, &T941_o1, T941_W);
	PUT_FIFO(T941_o0, 2);
	PUT_FIFO(T941_o1, 3);

	GET_FIFO(T942_i0, 1);
	GET_FIFO(T942_i1, 3);
	Butterfly(T942_i0, T942_i1, &T942_o0, &T942_o1, T942_W);
	PUT_FIFO(T942_o0, 2);
	PUT_FIFO(T942_o1, 3);

	GET_FIFO(T943_i0, 1);
	GET_FIFO(T943_i1, 3);
	Butterfly(T943_i0, T943_i1, &T943_o0, &T943_o1, T943_W);
	PUT_FIFO(T943_o0, 2);
	PUT_FIFO(T943_o1, 3);

	GET_FIFO(T944_i0, 0);
	GET_FIFO(T944_i1, 2);
	Butterfly(T944_i0, T944_i1, &T944_o0, &T944_o1, T944_W);
	PUT_FIFO(T944_o0, 0);
	PUT_FIFO(T944_o1, 1);

	GET_FIFO(T945_i0, 0);
	GET_FIFO(T945_i1, 2);
	Butterfly(T945_i0, T945_i1, &T945_o0, &T945_o1, T945_W);
	PUT_FIFO(T945_o0, 0);
	PUT_FIFO(T945_o1, 1);

	GET_FIFO(T946_i0, 0);
	GET_FIFO(T946_i1, 2);
	Butterfly(T946_i0, T946_i1, &T946_o0, &T946_o1, T946_W);
	PUT_FIFO(T946_o0, 0);
	PUT_FIFO(T946_o1, 1);

	GET_FIFO(T947_i0, 0);
	GET_FIFO(T947_i1, 2);
	Butterfly(T947_i0, T947_i1, &T947_o0, &T947_o1, T947_W);
	PUT_FIFO(T947_o0, 0);
	PUT_FIFO(T947_o1, 1);

	GET_FIFO(T948_i0, 1);
	GET_FIFO(T948_i1, 3);
	Butterfly(T948_i0, T948_i1, &T948_o0, &T948_o1, T948_W);
	PUT_FIFO(T948_o0, 0);
	PUT_FIFO(T948_o1, 1);

	GET_FIFO(T949_i0, 1);
	GET_FIFO(T949_i1, 3);
	Butterfly(T949_i0, T949_i1, &T949_o0, &T949_o1, T949_W);
	PUT_FIFO(T949_o0, 0);
	PUT_FIFO(T949_o1, 1);

	GET_FIFO(T950_i0, 1);
	GET_FIFO(T950_i1, 3);
	Butterfly(T950_i0, T950_i1, &T950_o0, &T950_o1, T950_W);
	PUT_FIFO(T950_o0, 0);
	PUT_FIFO(T950_o1, 1);

	GET_FIFO(T951_i0, 1);
	GET_FIFO(T951_i1, 3);
	Butterfly(T951_i0, T951_i1, &T951_o0, &T951_o1, T951_W);
	PUT_FIFO(T951_o0, 0);
	PUT_FIFO(T951_o1, 1);

	GET_FIFO(T952_i0, 0);
	GET_FIFO(T952_i1, 2);
	Butterfly(T952_i0, T952_i1, &T952_o0, &T952_o1, T952_W);
	PUT_FIFO(T952_o0, 2);
	PUT_FIFO(T952_o1, 3);

	GET_FIFO(T953_i0, 0);
	GET_FIFO(T953_i1, 2);
	Butterfly(T953_i0, T953_i1, &T953_o0, &T953_o1, T953_W);
	PUT_FIFO(T953_o0, 2);
	PUT_FIFO(T953_o1, 3);

	GET_FIFO(T954_i0, 0);
	GET_FIFO(T954_i1, 2);
	Butterfly(T954_i0, T954_i1, &T954_o0, &T954_o1, T954_W);
	PUT_FIFO(T954_o0, 2);
	PUT_FIFO(T954_o1, 3);

	GET_FIFO(T955_i0, 0);
	GET_FIFO(T955_i1, 2);
	Butterfly(T955_i0, T955_i1, &T955_o0, &T955_o1, T955_W);
	PUT_FIFO(T955_o0, 2);
	PUT_FIFO(T955_o1, 3);

	GET_FIFO(T956_i0, 1);
	GET_FIFO(T956_i1, 3);
	Butterfly(T956_i0, T956_i1, &T956_o0, &T956_o1, T956_W);
	PUT_FIFO(T956_o0, 2);
	PUT_FIFO(T956_o1, 3);

	GET_FIFO(T957_i0, 1);
	GET_FIFO(T957_i1, 3);
	Butterfly(T957_i0, T957_i1, &T957_o0, &T957_o1, T957_W);
	PUT_FIFO(T957_o0, 2);
	PUT_FIFO(T957_o1, 3);

	GET_FIFO(T958_i0, 1);
	GET_FIFO(T958_i1, 3);
	Butterfly(T958_i0, T958_i1, &T958_o0, &T958_o1, T958_W);
	PUT_FIFO(T958_o0, 2);
	PUT_FIFO(T958_o1, 3);

	GET_FIFO(T959_i0, 1);
	GET_FIFO(T959_i1, 3);
	Butterfly(T959_i0, T959_i1, &T959_o0, &T959_o1, T959_W);
	PUT_FIFO(T959_o0, 2);
	PUT_FIFO(T959_o1, 3);

	GET_FIFO(T960_i0, 0);
	GET_FIFO(T960_i1, 2);
	Butterfly(T960_i0, T960_i1, &T960_o0, &T960_o1, T960_W);
	PUT_FIFO(T960_o0, 0);
	PUT_FIFO(T960_o1, 1);

	GET_FIFO(T961_i0, 0);
	GET_FIFO(T961_i1, 2);
	Butterfly(T961_i0, T961_i1, &T961_o0, &T961_o1, T961_W);
	PUT_FIFO(T961_o0, 0);
	PUT_FIFO(T961_o1, 1);

	GET_FIFO(T962_i0, 0);
	GET_FIFO(T962_i1, 2);
	Butterfly(T962_i0, T962_i1, &T962_o0, &T962_o1, T962_W);
	PUT_FIFO(T962_o0, 0);
	PUT_FIFO(T962_o1, 1);

	GET_FIFO(T963_i0, 0);
	GET_FIFO(T963_i1, 2);
	Butterfly(T963_i0, T963_i1, &T963_o0, &T963_o1, T963_W);
	PUT_FIFO(T963_o0, 0);
	PUT_FIFO(T963_o1, 1);

	GET_FIFO(T964_i0, 1);
	GET_FIFO(T964_i1, 3);
	Butterfly(T964_i0, T964_i1, &T964_o0, &T964_o1, T964_W);
	PUT_FIFO(T964_o0, 0);
	PUT_FIFO(T964_o1, 1);

	GET_FIFO(T965_i0, 1);
	GET_FIFO(T965_i1, 3);
	Butterfly(T965_i0, T965_i1, &T965_o0, &T965_o1, T965_W);
	PUT_FIFO(T965_o0, 0);
	PUT_FIFO(T965_o1, 1);

	GET_FIFO(T966_i0, 1);
	GET_FIFO(T966_i1, 3);
	Butterfly(T966_i0, T966_i1, &T966_o0, &T966_o1, T966_W);
	PUT_FIFO(T966_o0, 0);
	PUT_FIFO(T966_o1, 1);

	GET_FIFO(T967_i0, 1);
	GET_FIFO(T967_i1, 3);
	Butterfly(T967_i0, T967_i1, &T967_o0, &T967_o1, T967_W);
	PUT_FIFO(T967_o0, 0);
	PUT_FIFO(T967_o1, 1);

	GET_FIFO(T968_i0, 0);
	GET_FIFO(T968_i1, 2);
	Butterfly(T968_i0, T968_i1, &T968_o0, &T968_o1, T968_W);
	PUT_FIFO(T968_o0, 2);
	PUT_FIFO(T968_o1, 3);

	GET_FIFO(T969_i0, 0);
	GET_FIFO(T969_i1, 2);
	Butterfly(T969_i0, T969_i1, &T969_o0, &T969_o1, T969_W);
	PUT_FIFO(T969_o0, 2);
	PUT_FIFO(T969_o1, 3);

	GET_FIFO(T970_i0, 0);
	GET_FIFO(T970_i1, 2);
	Butterfly(T970_i0, T970_i1, &T970_o0, &T970_o1, T970_W);
	PUT_FIFO(T970_o0, 2);
	PUT_FIFO(T970_o1, 3);

	GET_FIFO(T971_i0, 0);
	GET_FIFO(T971_i1, 2);
	Butterfly(T971_i0, T971_i1, &T971_o0, &T971_o1, T971_W);
	PUT_FIFO(T971_o0, 2);
	PUT_FIFO(T971_o1, 3);

	GET_FIFO(T972_i0, 1);
	GET_FIFO(T972_i1, 3);
	Butterfly(T972_i0, T972_i1, &T972_o0, &T972_o1, T972_W);
	PUT_FIFO(T972_o0, 2);
	PUT_FIFO(T972_o1, 3);

	GET_FIFO(T973_i0, 1);
	GET_FIFO(T973_i1, 3);
	Butterfly(T973_i0, T973_i1, &T973_o0, &T973_o1, T973_W);
	PUT_FIFO(T973_o0, 2);
	PUT_FIFO(T973_o1, 3);

	GET_FIFO(T974_i0, 1);
	GET_FIFO(T974_i1, 3);
	Butterfly(T974_i0, T974_i1, &T974_o0, &T974_o1, T974_W);
	PUT_FIFO(T974_o0, 2);
	PUT_FIFO(T974_o1, 3);

	GET_FIFO(T975_i0, 1);
	GET_FIFO(T975_i1, 3);
	Butterfly(T975_i0, T975_i1, &T975_o0, &T975_o1, T975_W);
	PUT_FIFO(T975_o0, 2);
	PUT_FIFO(T975_o1, 3);

	GET_FIFO(T976_i0, 0);
	GET_FIFO(T976_i1, 2);
	Butterfly(T976_i0, T976_i1, &T976_o0, &T976_o1, T976_W);
	PUT_FIFO(T976_o0, 0);
	PUT_FIFO(T976_o1, 1);

	GET_FIFO(T977_i0, 0);
	GET_FIFO(T977_i1, 2);
	Butterfly(T977_i0, T977_i1, &T977_o0, &T977_o1, T977_W);
	PUT_FIFO(T977_o0, 0);
	PUT_FIFO(T977_o1, 1);

	GET_FIFO(T978_i0, 0);
	GET_FIFO(T978_i1, 2);
	Butterfly(T978_i0, T978_i1, &T978_o0, &T978_o1, T978_W);
	PUT_FIFO(T978_o0, 0);
	PUT_FIFO(T978_o1, 1);

	GET_FIFO(T979_i0, 0);
	GET_FIFO(T979_i1, 2);
	Butterfly(T979_i0, T979_i1, &T979_o0, &T979_o1, T979_W);
	PUT_FIFO(T979_o0, 0);
	PUT_FIFO(T979_o1, 1);

	GET_FIFO(T980_i0, 1);
	GET_FIFO(T980_i1, 3);
	Butterfly(T980_i0, T980_i1, &T980_o0, &T980_o1, T980_W);
	PUT_FIFO(T980_o0, 0);
	PUT_FIFO(T980_o1, 1);

	GET_FIFO(T981_i0, 1);
	GET_FIFO(T981_i1, 3);
	Butterfly(T981_i0, T981_i1, &T981_o0, &T981_o1, T981_W);
	PUT_FIFO(T981_o0, 0);
	PUT_FIFO(T981_o1, 1);

	GET_FIFO(T982_i0, 1);
	GET_FIFO(T982_i1, 3);
	Butterfly(T982_i0, T982_i1, &T982_o0, &T982_o1, T982_W);
	PUT_FIFO(T982_o0, 0);
	PUT_FIFO(T982_o1, 1);

	GET_FIFO(T983_i0, 1);
	GET_FIFO(T983_i1, 3);
	Butterfly(T983_i0, T983_i1, &T983_o0, &T983_o1, T983_W);
	PUT_FIFO(T983_o0, 0);
	PUT_FIFO(T983_o1, 1);

	GET_FIFO(T984_i0, 0);
	GET_FIFO(T984_i1, 2);
	Butterfly(T984_i0, T984_i1, &T984_o0, &T984_o1, T984_W);
	PUT_FIFO(T984_o0, 2);
	PUT_FIFO(T984_o1, 3);

	GET_FIFO(T985_i0, 0);
	GET_FIFO(T985_i1, 2);
	Butterfly(T985_i0, T985_i1, &T985_o0, &T985_o1, T985_W);
	PUT_FIFO(T985_o0, 2);
	PUT_FIFO(T985_o1, 3);

	GET_FIFO(T986_i0, 0);
	GET_FIFO(T986_i1, 2);
	Butterfly(T986_i0, T986_i1, &T986_o0, &T986_o1, T986_W);
	PUT_FIFO(T986_o0, 2);
	PUT_FIFO(T986_o1, 3);

	GET_FIFO(T987_i0, 0);
	GET_FIFO(T987_i1, 2);
	Butterfly(T987_i0, T987_i1, &T987_o0, &T987_o1, T987_W);
	PUT_FIFO(T987_o0, 2);
	PUT_FIFO(T987_o1, 3);

	GET_FIFO(T988_i0, 1);
	GET_FIFO(T988_i1, 3);
	Butterfly(T988_i0, T988_i1, &T988_o0, &T988_o1, T988_W);
	PUT_FIFO(T988_o0, 2);
	PUT_FIFO(T988_o1, 3);

	GET_FIFO(T989_i0, 1);
	GET_FIFO(T989_i1, 3);
	Butterfly(T989_i0, T989_i1, &T989_o0, &T989_o1, T989_W);
	PUT_FIFO(T989_o0, 2);
	PUT_FIFO(T989_o1, 3);

	GET_FIFO(T990_i0, 1);
	GET_FIFO(T990_i1, 3);
	Butterfly(T990_i0, T990_i1, &T990_o0, &T990_o1, T990_W);
	PUT_FIFO(T990_o0, 2);
	PUT_FIFO(T990_o1, 3);

	GET_FIFO(T991_i0, 1);
	GET_FIFO(T991_i1, 3);
	Butterfly(T991_i0, T991_i1, &T991_o0, &T991_o1, T991_W);
	PUT_FIFO(T991_o0, 2);
	PUT_FIFO(T991_o1, 3);

	GET_FIFO(T992_i0, 0);
	GET_FIFO(T992_i1, 2);
	Butterfly(T992_i0, T992_i1, &T992_o0, &T992_o1, T992_W);
	PUT_FIFO(T992_o0, 0);
	PUT_FIFO(T992_o1, 1);

	GET_FIFO(T993_i0, 0);
	GET_FIFO(T993_i1, 2);
	Butterfly(T993_i0, T993_i1, &T993_o0, &T993_o1, T993_W);
	PUT_FIFO(T993_o0, 0);
	PUT_FIFO(T993_o1, 1);

	GET_FIFO(T994_i0, 0);
	GET_FIFO(T994_i1, 2);
	Butterfly(T994_i0, T994_i1, &T994_o0, &T994_o1, T994_W);
	PUT_FIFO(T994_o0, 0);
	PUT_FIFO(T994_o1, 1);

	GET_FIFO(T995_i0, 0);
	GET_FIFO(T995_i1, 2);
	Butterfly(T995_i0, T995_i1, &T995_o0, &T995_o1, T995_W);
	PUT_FIFO(T995_o0, 0);
	PUT_FIFO(T995_o1, 1);

	GET_FIFO(T996_i0, 1);
	GET_FIFO(T996_i1, 3);
	Butterfly(T996_i0, T996_i1, &T996_o0, &T996_o1, T996_W);
	PUT_FIFO(T996_o0, 0);
	PUT_FIFO(T996_o1, 1);

	GET_FIFO(T997_i0, 1);
	GET_FIFO(T997_i1, 3);
	Butterfly(T997_i0, T997_i1, &T997_o0, &T997_o1, T997_W);
	PUT_FIFO(T997_o0, 0);
	PUT_FIFO(T997_o1, 1);

	GET_FIFO(T998_i0, 1);
	GET_FIFO(T998_i1, 3);
	Butterfly(T998_i0, T998_i1, &T998_o0, &T998_o1, T998_W);
	PUT_FIFO(T998_o0, 0);
	PUT_FIFO(T998_o1, 1);

	GET_FIFO(T999_i0, 1);
	GET_FIFO(T999_i1, 3);
	Butterfly(T999_i0, T999_i1, &T999_o0, &T999_o1, T999_W);
	PUT_FIFO(T999_o0, 0);
	PUT_FIFO(T999_o1, 1);

	GET_FIFO(T1000_i0, 0);
	GET_FIFO(T1000_i1, 2);
	Butterfly(T1000_i0, T1000_i1, &T1000_o0, &T1000_o1, T1000_W);
	PUT_FIFO(T1000_o0, 2);
	PUT_FIFO(T1000_o1, 3);

	GET_FIFO(T1001_i0, 0);
	GET_FIFO(T1001_i1, 2);
	Butterfly(T1001_i0, T1001_i1, &T1001_o0, &T1001_o1, T1001_W);
	PUT_FIFO(T1001_o0, 2);
	PUT_FIFO(T1001_o1, 3);

	GET_FIFO(T1002_i0, 0);
	GET_FIFO(T1002_i1, 2);
	Butterfly(T1002_i0, T1002_i1, &T1002_o0, &T1002_o1, T1002_W);
	PUT_FIFO(T1002_o0, 2);
	PUT_FIFO(T1002_o1, 3);

	GET_FIFO(T1003_i0, 0);
	GET_FIFO(T1003_i1, 2);
	Butterfly(T1003_i0, T1003_i1, &T1003_o0, &T1003_o1, T1003_W);
	PUT_FIFO(T1003_o0, 2);
	PUT_FIFO(T1003_o1, 3);

	GET_FIFO(T1004_i0, 1);
	GET_FIFO(T1004_i1, 3);
	Butterfly(T1004_i0, T1004_i1, &T1004_o0, &T1004_o1, T1004_W);
	PUT_FIFO(T1004_o0, 2);
	PUT_FIFO(T1004_o1, 3);

	GET_FIFO(T1005_i0, 1);
	GET_FIFO(T1005_i1, 3);
	Butterfly(T1005_i0, T1005_i1, &T1005_o0, &T1005_o1, T1005_W);
	PUT_FIFO(T1005_o0, 2);
	PUT_FIFO(T1005_o1, 3);

	GET_FIFO(T1006_i0, 1);
	GET_FIFO(T1006_i1, 3);
	Butterfly(T1006_i0, T1006_i1, &T1006_o0, &T1006_o1, T1006_W);
	PUT_FIFO(T1006_o0, 2);
	PUT_FIFO(T1006_o1, 3);

	GET_FIFO(T1007_i0, 1);
	GET_FIFO(T1007_i1, 3);
	Butterfly(T1007_i0, T1007_i1, &T1007_o0, &T1007_o1, T1007_W);
	PUT_FIFO(T1007_o0, 2);
	PUT_FIFO(T1007_o1, 3);

	GET_FIFO(T1008_i0, 0);
	GET_FIFO(T1008_i1, 2);
	Butterfly(T1008_i0, T1008_i1, &T1008_o0, &T1008_o1, T1008_W);
	PUT_FIFO(T1008_o0, 0);
	PUT_FIFO(T1008_o1, 1);

	GET_FIFO(T1009_i0, 0);
	GET_FIFO(T1009_i1, 2);
	Butterfly(T1009_i0, T1009_i1, &T1009_o0, &T1009_o1, T1009_W);
	PUT_FIFO(T1009_o0, 0);
	PUT_FIFO(T1009_o1, 1);

	GET_FIFO(T1010_i0, 0);
	GET_FIFO(T1010_i1, 2);
	Butterfly(T1010_i0, T1010_i1, &T1010_o0, &T1010_o1, T1010_W);
	PUT_FIFO(T1010_o0, 0);
	PUT_FIFO(T1010_o1, 1);

	GET_FIFO(T1011_i0, 0);
	GET_FIFO(T1011_i1, 2);
	Butterfly(T1011_i0, T1011_i1, &T1011_o0, &T1011_o1, T1011_W);
	PUT_FIFO(T1011_o0, 0);
	PUT_FIFO(T1011_o1, 1);

	GET_FIFO(T1012_i0, 1);
	GET_FIFO(T1012_i1, 3);
	Butterfly(T1012_i0, T1012_i1, &T1012_o0, &T1012_o1, T1012_W);
	PUT_FIFO(T1012_o0, 0);
	PUT_FIFO(T1012_o1, 1);

	GET_FIFO(T1013_i0, 1);
	GET_FIFO(T1013_i1, 3);
	Butterfly(T1013_i0, T1013_i1, &T1013_o0, &T1013_o1, T1013_W);
	PUT_FIFO(T1013_o0, 0);
	PUT_FIFO(T1013_o1, 1);

	GET_FIFO(T1014_i0, 1);
	GET_FIFO(T1014_i1, 3);
	Butterfly(T1014_i0, T1014_i1, &T1014_o0, &T1014_o1, T1014_W);
	PUT_FIFO(T1014_o0, 0);
	PUT_FIFO(T1014_o1, 1);

	GET_FIFO(T1015_i0, 1);
	GET_FIFO(T1015_i1, 3);
	Butterfly(T1015_i0, T1015_i1, &T1015_o0, &T1015_o1, T1015_W);
	PUT_FIFO(T1015_o0, 0);
	PUT_FIFO(T1015_o1, 1);

	GET_FIFO(T1016_i0, 0);
	GET_FIFO(T1016_i1, 2);
	Butterfly(T1016_i0, T1016_i1, &T1016_o0, &T1016_o1, T1016_W);
	PUT_FIFO(T1016_o0, 2);
	PUT_FIFO(T1016_o1, 3);

	GET_FIFO(T1017_i0, 0);
	GET_FIFO(T1017_i1, 2);
	Butterfly(T1017_i0, T1017_i1, &T1017_o0, &T1017_o1, T1017_W);
	PUT_FIFO(T1017_o0, 2);
	PUT_FIFO(T1017_o1, 3);

	GET_FIFO(T1018_i0, 0);
	GET_FIFO(T1018_i1, 2);
	Butterfly(T1018_i0, T1018_i1, &T1018_o0, &T1018_o1, T1018_W);
	PUT_FIFO(T1018_o0, 2);
	PUT_FIFO(T1018_o1, 3);

	GET_FIFO(T1019_i0, 0);
	GET_FIFO(T1019_i1, 2);
	Butterfly(T1019_i0, T1019_i1, &T1019_o0, &T1019_o1, T1019_W);
	PUT_FIFO(T1019_o0, 2);
	PUT_FIFO(T1019_o1, 3);

	GET_FIFO(T1020_i0, 1);
	GET_FIFO(T1020_i1, 3);
	Butterfly(T1020_i0, T1020_i1, &T1020_o0, &T1020_o1, T1020_W);
	PUT_FIFO(T1020_o0, 2);
	PUT_FIFO(T1020_o1, 3);

	GET_FIFO(T1021_i0, 1);
	GET_FIFO(T1021_i1, 3);
	Butterfly(T1021_i0, T1021_i1, &T1021_o0, &T1021_o1, T1021_W);
	PUT_FIFO(T1021_o0, 2);
	PUT_FIFO(T1021_o1, 3);

	GET_FIFO(T1022_i0, 1);
	GET_FIFO(T1022_i1, 3);
	Butterfly(T1022_i0, T1022_i1, &T1022_o0, &T1022_o1, T1022_W);
	PUT_FIFO(T1022_o0, 2);
	PUT_FIFO(T1022_o1, 3);

	GET_FIFO(T1023_i0, 1);
	GET_FIFO(T1023_i1, 3);
	Butterfly(T1023_i0, T1023_i1, &T1023_o0, &T1023_o1, T1023_W);
	PUT_FIFO(T1023_o0, 2);
	PUT_FIFO(T1023_o1, 3);
}
