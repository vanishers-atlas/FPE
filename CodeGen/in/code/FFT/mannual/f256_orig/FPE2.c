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
void FPE2PE0() {

  // **** Variable declaration **** //
	int T512_i0;
	int T512_i1;
	int T512_o0;
	int T512_o1;
	int T512_W;

	int T513_i0;
	int T513_i1;
	int T513_o0;
	int T513_o1;
	int T513_W;

	int T514_i0;
	int T514_i1;
	int T514_o0;
	int T514_o1;
	int T514_W;

	int T515_i0;
	int T515_i1;
	int T515_o0;
	int T515_o1;
	int T515_W;

	int T516_i0;
	int T516_i1;
	int T516_o0;
	int T516_o1;
	int T516_W;

	int T517_i0;
	int T517_i1;
	int T517_o0;
	int T517_o1;
	int T517_W;

	int T518_i0;
	int T518_i1;
	int T518_o0;
	int T518_o1;
	int T518_W;

	int T519_i0;
	int T519_i1;
	int T519_o0;
	int T519_o1;
	int T519_W;

	int T520_i0;
	int T520_i1;
	int T520_o0;
	int T520_o1;
	int T520_W;

	int T521_i0;
	int T521_i1;
	int T521_o0;
	int T521_o1;
	int T521_W;

	int T522_i0;
	int T522_i1;
	int T522_o0;
	int T522_o1;
	int T522_W;

	int T523_i0;
	int T523_i1;
	int T523_o0;
	int T523_o1;
	int T523_W;

	int T524_i0;
	int T524_i1;
	int T524_o0;
	int T524_o1;
	int T524_W;

	int T525_i0;
	int T525_i1;
	int T525_o0;
	int T525_o1;
	int T525_W;

	int T526_i0;
	int T526_i1;
	int T526_o0;
	int T526_o1;
	int T526_W;

	int T527_i0;
	int T527_i1;
	int T527_o0;
	int T527_o1;
	int T527_W;

	int T528_i0;
	int T528_i1;
	int T528_o0;
	int T528_o1;
	int T528_W;

	int T529_i0;
	int T529_i1;
	int T529_o0;
	int T529_o1;
	int T529_W;

	int T530_i0;
	int T530_i1;
	int T530_o0;
	int T530_o1;
	int T530_W;

	int T531_i0;
	int T531_i1;
	int T531_o0;
	int T531_o1;
	int T531_W;

	int T532_i0;
	int T532_i1;
	int T532_o0;
	int T532_o1;
	int T532_W;

	int T533_i0;
	int T533_i1;
	int T533_o0;
	int T533_o1;
	int T533_W;

	int T534_i0;
	int T534_i1;
	int T534_o0;
	int T534_o1;
	int T534_W;

	int T535_i0;
	int T535_i1;
	int T535_o0;
	int T535_o1;
	int T535_W;

	int T536_i0;
	int T536_i1;
	int T536_o0;
	int T536_o1;
	int T536_W;

	int T537_i0;
	int T537_i1;
	int T537_o0;
	int T537_o1;
	int T537_W;

	int T538_i0;
	int T538_i1;
	int T538_o0;
	int T538_o1;
	int T538_W;

	int T539_i0;
	int T539_i1;
	int T539_o0;
	int T539_o1;
	int T539_W;

	int T540_i0;
	int T540_i1;
	int T540_o0;
	int T540_o1;
	int T540_W;

	int T541_i0;
	int T541_i1;
	int T541_o0;
	int T541_o1;
	int T541_W;

	int T542_i0;
	int T542_i1;
	int T542_o0;
	int T542_o1;
	int T542_W;

	int T543_i0;
	int T543_i1;
	int T543_o0;
	int T543_o1;
	int T543_W;

	int T544_i0;
	int T544_i1;
	int T544_o0;
	int T544_o1;
	int T544_W;

	int T545_i0;
	int T545_i1;
	int T545_o0;
	int T545_o1;
	int T545_W;

	int T546_i0;
	int T546_i1;
	int T546_o0;
	int T546_o1;
	int T546_W;

	int T547_i0;
	int T547_i1;
	int T547_o0;
	int T547_o1;
	int T547_W;

	int T548_i0;
	int T548_i1;
	int T548_o0;
	int T548_o1;
	int T548_W;

	int T549_i0;
	int T549_i1;
	int T549_o0;
	int T549_o1;
	int T549_W;

	int T550_i0;
	int T550_i1;
	int T550_o0;
	int T550_o1;
	int T550_W;

	int T551_i0;
	int T551_i1;
	int T551_o0;
	int T551_o1;
	int T551_W;

	int T552_i0;
	int T552_i1;
	int T552_o0;
	int T552_o1;
	int T552_W;

	int T553_i0;
	int T553_i1;
	int T553_o0;
	int T553_o1;
	int T553_W;

	int T554_i0;
	int T554_i1;
	int T554_o0;
	int T554_o1;
	int T554_W;

	int T555_i0;
	int T555_i1;
	int T555_o0;
	int T555_o1;
	int T555_W;

	int T556_i0;
	int T556_i1;
	int T556_o0;
	int T556_o1;
	int T556_W;

	int T557_i0;
	int T557_i1;
	int T557_o0;
	int T557_o1;
	int T557_W;

	int T558_i0;
	int T558_i1;
	int T558_o0;
	int T558_o1;
	int T558_W;

	int T559_i0;
	int T559_i1;
	int T559_o0;
	int T559_o1;
	int T559_W;

	int T560_i0;
	int T560_i1;
	int T560_o0;
	int T560_o1;
	int T560_W;

	int T561_i0;
	int T561_i1;
	int T561_o0;
	int T561_o1;
	int T561_W;

	int T562_i0;
	int T562_i1;
	int T562_o0;
	int T562_o1;
	int T562_W;

	int T563_i0;
	int T563_i1;
	int T563_o0;
	int T563_o1;
	int T563_W;

	int T564_i0;
	int T564_i1;
	int T564_o0;
	int T564_o1;
	int T564_W;

	int T565_i0;
	int T565_i1;
	int T565_o0;
	int T565_o1;
	int T565_W;

	int T566_i0;
	int T566_i1;
	int T566_o0;
	int T566_o1;
	int T566_W;

	int T567_i0;
	int T567_i1;
	int T567_o0;
	int T567_o1;
	int T567_W;

	int T568_i0;
	int T568_i1;
	int T568_o0;
	int T568_o1;
	int T568_W;

	int T569_i0;
	int T569_i1;
	int T569_o0;
	int T569_o1;
	int T569_W;

	int T570_i0;
	int T570_i1;
	int T570_o0;
	int T570_o1;
	int T570_W;

	int T571_i0;
	int T571_i1;
	int T571_o0;
	int T571_o1;
	int T571_W;

	int T572_i0;
	int T572_i1;
	int T572_o0;
	int T572_o1;
	int T572_W;

	int T573_i0;
	int T573_i1;
	int T573_o0;
	int T573_o1;
	int T573_W;

	int T574_i0;
	int T574_i1;
	int T574_o0;
	int T574_o1;
	int T574_W;

	int T575_i0;
	int T575_i1;
	int T575_o0;
	int T575_o1;
	int T575_W;

	int T576_i0;
	int T576_i1;
	int T576_o0;
	int T576_o1;
	int T576_W;

	int T577_i0;
	int T577_i1;
	int T577_o0;
	int T577_o1;
	int T577_W;

	int T578_i0;
	int T578_i1;
	int T578_o0;
	int T578_o1;
	int T578_W;

	int T579_i0;
	int T579_i1;
	int T579_o0;
	int T579_o1;
	int T579_W;

	int T580_i0;
	int T580_i1;
	int T580_o0;
	int T580_o1;
	int T580_W;

	int T581_i0;
	int T581_i1;
	int T581_o0;
	int T581_o1;
	int T581_W;

	int T582_i0;
	int T582_i1;
	int T582_o0;
	int T582_o1;
	int T582_W;

	int T583_i0;
	int T583_i1;
	int T583_o0;
	int T583_o1;
	int T583_W;

	int T584_i0;
	int T584_i1;
	int T584_o0;
	int T584_o1;
	int T584_W;

	int T585_i0;
	int T585_i1;
	int T585_o0;
	int T585_o1;
	int T585_W;

	int T586_i0;
	int T586_i1;
	int T586_o0;
	int T586_o1;
	int T586_W;

	int T587_i0;
	int T587_i1;
	int T587_o0;
	int T587_o1;
	int T587_W;

	int T588_i0;
	int T588_i1;
	int T588_o0;
	int T588_o1;
	int T588_W;

	int T589_i0;
	int T589_i1;
	int T589_o0;
	int T589_o1;
	int T589_W;

	int T590_i0;
	int T590_i1;
	int T590_o0;
	int T590_o1;
	int T590_W;

	int T591_i0;
	int T591_i1;
	int T591_o0;
	int T591_o1;
	int T591_W;

	int T592_i0;
	int T592_i1;
	int T592_o0;
	int T592_o1;
	int T592_W;

	int T593_i0;
	int T593_i1;
	int T593_o0;
	int T593_o1;
	int T593_W;

	int T594_i0;
	int T594_i1;
	int T594_o0;
	int T594_o1;
	int T594_W;

	int T595_i0;
	int T595_i1;
	int T595_o0;
	int T595_o1;
	int T595_W;

	int T596_i0;
	int T596_i1;
	int T596_o0;
	int T596_o1;
	int T596_W;

	int T597_i0;
	int T597_i1;
	int T597_o0;
	int T597_o1;
	int T597_W;

	int T598_i0;
	int T598_i1;
	int T598_o0;
	int T598_o1;
	int T598_W;

	int T599_i0;
	int T599_i1;
	int T599_o0;
	int T599_o1;
	int T599_W;

	int T600_i0;
	int T600_i1;
	int T600_o0;
	int T600_o1;
	int T600_W;

	int T601_i0;
	int T601_i1;
	int T601_o0;
	int T601_o1;
	int T601_W;

	int T602_i0;
	int T602_i1;
	int T602_o0;
	int T602_o1;
	int T602_W;

	int T603_i0;
	int T603_i1;
	int T603_o0;
	int T603_o1;
	int T603_W;

	int T604_i0;
	int T604_i1;
	int T604_o0;
	int T604_o1;
	int T604_W;

	int T605_i0;
	int T605_i1;
	int T605_o0;
	int T605_o1;
	int T605_W;

	int T606_i0;
	int T606_i1;
	int T606_o0;
	int T606_o1;
	int T606_W;

	int T607_i0;
	int T607_i1;
	int T607_o0;
	int T607_o1;
	int T607_W;

	int T608_i0;
	int T608_i1;
	int T608_o0;
	int T608_o1;
	int T608_W;

	int T609_i0;
	int T609_i1;
	int T609_o0;
	int T609_o1;
	int T609_W;

	int T610_i0;
	int T610_i1;
	int T610_o0;
	int T610_o1;
	int T610_W;

	int T611_i0;
	int T611_i1;
	int T611_o0;
	int T611_o1;
	int T611_W;

	int T612_i0;
	int T612_i1;
	int T612_o0;
	int T612_o1;
	int T612_W;

	int T613_i0;
	int T613_i1;
	int T613_o0;
	int T613_o1;
	int T613_W;

	int T614_i0;
	int T614_i1;
	int T614_o0;
	int T614_o1;
	int T614_W;

	int T615_i0;
	int T615_i1;
	int T615_o0;
	int T615_o1;
	int T615_W;

	int T616_i0;
	int T616_i1;
	int T616_o0;
	int T616_o1;
	int T616_W;

	int T617_i0;
	int T617_i1;
	int T617_o0;
	int T617_o1;
	int T617_W;

	int T618_i0;
	int T618_i1;
	int T618_o0;
	int T618_o1;
	int T618_W;

	int T619_i0;
	int T619_i1;
	int T619_o0;
	int T619_o1;
	int T619_W;

	int T620_i0;
	int T620_i1;
	int T620_o0;
	int T620_o1;
	int T620_W;

	int T621_i0;
	int T621_i1;
	int T621_o0;
	int T621_o1;
	int T621_W;

	int T622_i0;
	int T622_i1;
	int T622_o0;
	int T622_o1;
	int T622_W;

	int T623_i0;
	int T623_i1;
	int T623_o0;
	int T623_o1;
	int T623_W;

	int T624_i0;
	int T624_i1;
	int T624_o0;
	int T624_o1;
	int T624_W;

	int T625_i0;
	int T625_i1;
	int T625_o0;
	int T625_o1;
	int T625_W;

	int T626_i0;
	int T626_i1;
	int T626_o0;
	int T626_o1;
	int T626_W;

	int T627_i0;
	int T627_i1;
	int T627_o0;
	int T627_o1;
	int T627_W;

	int T628_i0;
	int T628_i1;
	int T628_o0;
	int T628_o1;
	int T628_W;

	int T629_i0;
	int T629_i1;
	int T629_o0;
	int T629_o1;
	int T629_W;

	int T630_i0;
	int T630_i1;
	int T630_o0;
	int T630_o1;
	int T630_W;

	int T631_i0;
	int T631_i1;
	int T631_o0;
	int T631_o1;
	int T631_W;

	int T632_i0;
	int T632_i1;
	int T632_o0;
	int T632_o1;
	int T632_W;

	int T633_i0;
	int T633_i1;
	int T633_o0;
	int T633_o1;
	int T633_W;

	int T634_i0;
	int T634_i1;
	int T634_o0;
	int T634_o1;
	int T634_W;

	int T635_i0;
	int T635_i1;
	int T635_o0;
	int T635_o1;
	int T635_W;

	int T636_i0;
	int T636_i1;
	int T636_o0;
	int T636_o1;
	int T636_W;

	int T637_i0;
	int T637_i1;
	int T637_o0;
	int T637_o1;
	int T637_W;

	int T638_i0;
	int T638_i1;
	int T638_o0;
	int T638_o1;
	int T638_W;

	int T639_i0;
	int T639_i1;
	int T639_o0;
	int T639_o1;
	int T639_W;

	int T640_i0;
	int T640_i1;
	int T640_o0;
	int T640_o1;
	int T640_W;

	int T641_i0;
	int T641_i1;
	int T641_o0;
	int T641_o1;
	int T641_W;

	int T642_i0;
	int T642_i1;
	int T642_o0;
	int T642_o1;
	int T642_W;

	int T643_i0;
	int T643_i1;
	int T643_o0;
	int T643_o1;
	int T643_W;

	int T644_i0;
	int T644_i1;
	int T644_o0;
	int T644_o1;
	int T644_W;

	int T645_i0;
	int T645_i1;
	int T645_o0;
	int T645_o1;
	int T645_W;

	int T646_i0;
	int T646_i1;
	int T646_o0;
	int T646_o1;
	int T646_W;

	int T647_i0;
	int T647_i1;
	int T647_o0;
	int T647_o1;
	int T647_W;

	int T648_i0;
	int T648_i1;
	int T648_o0;
	int T648_o1;
	int T648_W;

	int T649_i0;
	int T649_i1;
	int T649_o0;
	int T649_o1;
	int T649_W;

	int T650_i0;
	int T650_i1;
	int T650_o0;
	int T650_o1;
	int T650_W;

	int T651_i0;
	int T651_i1;
	int T651_o0;
	int T651_o1;
	int T651_W;

	int T652_i0;
	int T652_i1;
	int T652_o0;
	int T652_o1;
	int T652_W;

	int T653_i0;
	int T653_i1;
	int T653_o0;
	int T653_o1;
	int T653_W;

	int T654_i0;
	int T654_i1;
	int T654_o0;
	int T654_o1;
	int T654_W;

	int T655_i0;
	int T655_i1;
	int T655_o0;
	int T655_o1;
	int T655_W;

	int T656_i0;
	int T656_i1;
	int T656_o0;
	int T656_o1;
	int T656_W;

	int T657_i0;
	int T657_i1;
	int T657_o0;
	int T657_o1;
	int T657_W;

	int T658_i0;
	int T658_i1;
	int T658_o0;
	int T658_o1;
	int T658_W;

	int T659_i0;
	int T659_i1;
	int T659_o0;
	int T659_o1;
	int T659_W;

	int T660_i0;
	int T660_i1;
	int T660_o0;
	int T660_o1;
	int T660_W;

	int T661_i0;
	int T661_i1;
	int T661_o0;
	int T661_o1;
	int T661_W;

	int T662_i0;
	int T662_i1;
	int T662_o0;
	int T662_o1;
	int T662_W;

	int T663_i0;
	int T663_i1;
	int T663_o0;
	int T663_o1;
	int T663_W;

	int T664_i0;
	int T664_i1;
	int T664_o0;
	int T664_o1;
	int T664_W;

	int T665_i0;
	int T665_i1;
	int T665_o0;
	int T665_o1;
	int T665_W;

	int T666_i0;
	int T666_i1;
	int T666_o0;
	int T666_o1;
	int T666_W;

	int T667_i0;
	int T667_i1;
	int T667_o0;
	int T667_o1;
	int T667_W;

	int T668_i0;
	int T668_i1;
	int T668_o0;
	int T668_o1;
	int T668_W;

	int T669_i0;
	int T669_i1;
	int T669_o0;
	int T669_o1;
	int T669_W;

	int T670_i0;
	int T670_i1;
	int T670_o0;
	int T670_o1;
	int T670_W;

	int T671_i0;
	int T671_i1;
	int T671_o0;
	int T671_o1;
	int T671_W;

	int T672_i0;
	int T672_i1;
	int T672_o0;
	int T672_o1;
	int T672_W;

	int T673_i0;
	int T673_i1;
	int T673_o0;
	int T673_o1;
	int T673_W;

	int T674_i0;
	int T674_i1;
	int T674_o0;
	int T674_o1;
	int T674_W;

	int T675_i0;
	int T675_i1;
	int T675_o0;
	int T675_o1;
	int T675_W;

	int T676_i0;
	int T676_i1;
	int T676_o0;
	int T676_o1;
	int T676_W;

	int T677_i0;
	int T677_i1;
	int T677_o0;
	int T677_o1;
	int T677_W;

	int T678_i0;
	int T678_i1;
	int T678_o0;
	int T678_o1;
	int T678_W;

	int T679_i0;
	int T679_i1;
	int T679_o0;
	int T679_o1;
	int T679_W;

	int T680_i0;
	int T680_i1;
	int T680_o0;
	int T680_o1;
	int T680_W;

	int T681_i0;
	int T681_i1;
	int T681_o0;
	int T681_o1;
	int T681_W;

	int T682_i0;
	int T682_i1;
	int T682_o0;
	int T682_o1;
	int T682_W;

	int T683_i0;
	int T683_i1;
	int T683_o0;
	int T683_o1;
	int T683_W;

	int T684_i0;
	int T684_i1;
	int T684_o0;
	int T684_o1;
	int T684_W;

	int T685_i0;
	int T685_i1;
	int T685_o0;
	int T685_o1;
	int T685_W;

	int T686_i0;
	int T686_i1;
	int T686_o0;
	int T686_o1;
	int T686_W;

	int T687_i0;
	int T687_i1;
	int T687_o0;
	int T687_o1;
	int T687_W;

	int T688_i0;
	int T688_i1;
	int T688_o0;
	int T688_o1;
	int T688_W;

	int T689_i0;
	int T689_i1;
	int T689_o0;
	int T689_o1;
	int T689_W;

	int T690_i0;
	int T690_i1;
	int T690_o0;
	int T690_o1;
	int T690_W;

	int T691_i0;
	int T691_i1;
	int T691_o0;
	int T691_o1;
	int T691_W;

	int T692_i0;
	int T692_i1;
	int T692_o0;
	int T692_o1;
	int T692_W;

	int T693_i0;
	int T693_i1;
	int T693_o0;
	int T693_o1;
	int T693_W;

	int T694_i0;
	int T694_i1;
	int T694_o0;
	int T694_o1;
	int T694_W;

	int T695_i0;
	int T695_i1;
	int T695_o0;
	int T695_o1;
	int T695_W;

	int T696_i0;
	int T696_i1;
	int T696_o0;
	int T696_o1;
	int T696_W;

	int T697_i0;
	int T697_i1;
	int T697_o0;
	int T697_o1;
	int T697_W;

	int T698_i0;
	int T698_i1;
	int T698_o0;
	int T698_o1;
	int T698_W;

	int T699_i0;
	int T699_i1;
	int T699_o0;
	int T699_o1;
	int T699_W;

	int T700_i0;
	int T700_i1;
	int T700_o0;
	int T700_o1;
	int T700_W;

	int T701_i0;
	int T701_i1;
	int T701_o0;
	int T701_o1;
	int T701_W;

	int T702_i0;
	int T702_i1;
	int T702_o0;
	int T702_o1;
	int T702_W;

	int T703_i0;
	int T703_i1;
	int T703_o0;
	int T703_o1;
	int T703_W;

	int T704_i0;
	int T704_i1;
	int T704_o0;
	int T704_o1;
	int T704_W;

	int T705_i0;
	int T705_i1;
	int T705_o0;
	int T705_o1;
	int T705_W;

	int T706_i0;
	int T706_i1;
	int T706_o0;
	int T706_o1;
	int T706_W;

	int T707_i0;
	int T707_i1;
	int T707_o0;
	int T707_o1;
	int T707_W;

	int T708_i0;
	int T708_i1;
	int T708_o0;
	int T708_o1;
	int T708_W;

	int T709_i0;
	int T709_i1;
	int T709_o0;
	int T709_o1;
	int T709_W;

	int T710_i0;
	int T710_i1;
	int T710_o0;
	int T710_o1;
	int T710_W;

	int T711_i0;
	int T711_i1;
	int T711_o0;
	int T711_o1;
	int T711_W;

	int T712_i0;
	int T712_i1;
	int T712_o0;
	int T712_o1;
	int T712_W;

	int T713_i0;
	int T713_i1;
	int T713_o0;
	int T713_o1;
	int T713_W;

	int T714_i0;
	int T714_i1;
	int T714_o0;
	int T714_o1;
	int T714_W;

	int T715_i0;
	int T715_i1;
	int T715_o0;
	int T715_o1;
	int T715_W;

	int T716_i0;
	int T716_i1;
	int T716_o0;
	int T716_o1;
	int T716_W;

	int T717_i0;
	int T717_i1;
	int T717_o0;
	int T717_o1;
	int T717_W;

	int T718_i0;
	int T718_i1;
	int T718_o0;
	int T718_o1;
	int T718_W;

	int T719_i0;
	int T719_i1;
	int T719_o0;
	int T719_o1;
	int T719_W;

	int T720_i0;
	int T720_i1;
	int T720_o0;
	int T720_o1;
	int T720_W;

	int T721_i0;
	int T721_i1;
	int T721_o0;
	int T721_o1;
	int T721_W;

	int T722_i0;
	int T722_i1;
	int T722_o0;
	int T722_o1;
	int T722_W;

	int T723_i0;
	int T723_i1;
	int T723_o0;
	int T723_o1;
	int T723_W;

	int T724_i0;
	int T724_i1;
	int T724_o0;
	int T724_o1;
	int T724_W;

	int T725_i0;
	int T725_i1;
	int T725_o0;
	int T725_o1;
	int T725_W;

	int T726_i0;
	int T726_i1;
	int T726_o0;
	int T726_o1;
	int T726_W;

	int T727_i0;
	int T727_i1;
	int T727_o0;
	int T727_o1;
	int T727_W;

	int T728_i0;
	int T728_i1;
	int T728_o0;
	int T728_o1;
	int T728_W;

	int T729_i0;
	int T729_i1;
	int T729_o0;
	int T729_o1;
	int T729_W;

	int T730_i0;
	int T730_i1;
	int T730_o0;
	int T730_o1;
	int T730_W;

	int T731_i0;
	int T731_i1;
	int T731_o0;
	int T731_o1;
	int T731_W;

	int T732_i0;
	int T732_i1;
	int T732_o0;
	int T732_o1;
	int T732_W;

	int T733_i0;
	int T733_i1;
	int T733_o0;
	int T733_o1;
	int T733_W;

	int T734_i0;
	int T734_i1;
	int T734_o0;
	int T734_o1;
	int T734_W;

	int T735_i0;
	int T735_i1;
	int T735_o0;
	int T735_o1;
	int T735_W;

	int T736_i0;
	int T736_i1;
	int T736_o0;
	int T736_o1;
	int T736_W;

	int T737_i0;
	int T737_i1;
	int T737_o0;
	int T737_o1;
	int T737_W;

	int T738_i0;
	int T738_i1;
	int T738_o0;
	int T738_o1;
	int T738_W;

	int T739_i0;
	int T739_i1;
	int T739_o0;
	int T739_o1;
	int T739_W;

	int T740_i0;
	int T740_i1;
	int T740_o0;
	int T740_o1;
	int T740_W;

	int T741_i0;
	int T741_i1;
	int T741_o0;
	int T741_o1;
	int T741_W;

	int T742_i0;
	int T742_i1;
	int T742_o0;
	int T742_o1;
	int T742_W;

	int T743_i0;
	int T743_i1;
	int T743_o0;
	int T743_o1;
	int T743_W;

	int T744_i0;
	int T744_i1;
	int T744_o0;
	int T744_o1;
	int T744_W;

	int T745_i0;
	int T745_i1;
	int T745_o0;
	int T745_o1;
	int T745_W;

	int T746_i0;
	int T746_i1;
	int T746_o0;
	int T746_o1;
	int T746_W;

	int T747_i0;
	int T747_i1;
	int T747_o0;
	int T747_o1;
	int T747_W;

	int T748_i0;
	int T748_i1;
	int T748_o0;
	int T748_o1;
	int T748_W;

	int T749_i0;
	int T749_i1;
	int T749_o0;
	int T749_o1;
	int T749_W;

	int T750_i0;
	int T750_i1;
	int T750_o0;
	int T750_o1;
	int T750_W;

	int T751_i0;
	int T751_i1;
	int T751_o0;
	int T751_o1;
	int T751_W;

	int T752_i0;
	int T752_i1;
	int T752_o0;
	int T752_o1;
	int T752_W;

	int T753_i0;
	int T753_i1;
	int T753_o0;
	int T753_o1;
	int T753_W;

	int T754_i0;
	int T754_i1;
	int T754_o0;
	int T754_o1;
	int T754_W;

	int T755_i0;
	int T755_i1;
	int T755_o0;
	int T755_o1;
	int T755_W;

	int T756_i0;
	int T756_i1;
	int T756_o0;
	int T756_o1;
	int T756_W;

	int T757_i0;
	int T757_i1;
	int T757_o0;
	int T757_o1;
	int T757_W;

	int T758_i0;
	int T758_i1;
	int T758_o0;
	int T758_o1;
	int T758_W;

	int T759_i0;
	int T759_i1;
	int T759_o0;
	int T759_o1;
	int T759_W;

	int T760_i0;
	int T760_i1;
	int T760_o0;
	int T760_o1;
	int T760_W;

	int T761_i0;
	int T761_i1;
	int T761_o0;
	int T761_o1;
	int T761_W;

	int T762_i0;
	int T762_i1;
	int T762_o0;
	int T762_o1;
	int T762_W;

	int T763_i0;
	int T763_i1;
	int T763_o0;
	int T763_o1;
	int T763_W;

	int T764_i0;
	int T764_i1;
	int T764_o0;
	int T764_o1;
	int T764_W;

	int T765_i0;
	int T765_i1;
	int T765_o0;
	int T765_o1;
	int T765_W;

	int T766_i0;
	int T766_i1;
	int T766_o0;
	int T766_o1;
	int T766_W;

	int T767_i0;
	int T767_i1;
	int T767_o0;
	int T767_o1;
	int T767_W;


  // **** Parameter initialisation **** //
T512_W = 16384;
T513_W = -759222975;
T514_W = -1073741824;
T515_W = -759246145;
T516_W = 16384;
T517_W = -759222975;
T518_W = -1073741824;
T519_W = -759246145;
T520_W = 16384;
T521_W = -759222975;
T522_W = -1073741824;
T523_W = -759246145;
T524_W = 16384;
T525_W = -759222975;
T526_W = -1073741824;
T527_W = -759246145;
T528_W = 16384;
T529_W = -759222975;
T530_W = -1073741824;
T531_W = -759246145;
T532_W = 16384;
T533_W = -759222975;
T534_W = -1073741824;
T535_W = -759246145;
T536_W = 16384;
T537_W = -759222975;
T538_W = -1073741824;
T539_W = -759246145;
T540_W = 16384;
T541_W = -759222975;
T542_W = -1073741824;
T543_W = -759246145;
T544_W = 16384;
T545_W = -759222975;
T546_W = -1073741824;
T547_W = -759246145;
T548_W = 16384;
T549_W = -759222975;
T550_W = -1073741824;
T551_W = -759246145;
T552_W = 16384;
T553_W = -759222975;
T554_W = -1073741824;
T555_W = -759246145;
T556_W = 16384;
T557_W = -759222975;
T558_W = -1073741824;
T559_W = -759246145;
T560_W = 16384;
T561_W = -759222975;
T562_W = -1073741824;
T563_W = -759246145;
T564_W = 16384;
T565_W = -759222975;
T566_W = -1073741824;
T567_W = -759246145;
T568_W = 16384;
T569_W = -759222975;
T570_W = -1073741824;
T571_W = -759246145;
T572_W = 16384;
T573_W = -759222975;
T574_W = -1073741824;
T575_W = -759246145;
T576_W = 16384;
T577_W = -759222975;
T578_W = -1073741824;
T579_W = -759246145;
T580_W = 16384;
T581_W = -759222975;
T582_W = -1073741824;
T583_W = -759246145;
T584_W = 16384;
T585_W = -759222975;
T586_W = -1073741824;
T587_W = -759246145;
T588_W = 16384;
T589_W = -759222975;
T590_W = -1073741824;
T591_W = -759246145;
T592_W = 16384;
T593_W = -759222975;
T594_W = -1073741824;
T595_W = -759246145;
T596_W = 16384;
T597_W = -759222975;
T598_W = -1073741824;
T599_W = -759246145;
T600_W = 16384;
T601_W = -759222975;
T602_W = -1073741824;
T603_W = -759246145;
T604_W = 16384;
T605_W = -759222975;
T606_W = -1073741824;
T607_W = -759246145;
T608_W = 16384;
T609_W = -759222975;
T610_W = -1073741824;
T611_W = -759246145;
T612_W = 16384;
T613_W = -759222975;
T614_W = -1073741824;
T615_W = -759246145;
T616_W = 16384;
T617_W = -759222975;
T618_W = -1073741824;
T619_W = -759246145;
T620_W = 16384;
T621_W = -759222975;
T622_W = -1073741824;
T623_W = -759246145;
T624_W = 16384;
T625_W = -759222975;
T626_W = -1073741824;
T627_W = -759246145;
T628_W = 16384;
T629_W = -759222975;
T630_W = -1073741824;
T631_W = -759246145;
T632_W = 16384;
T633_W = -759222975;
T634_W = -1073741824;
T635_W = -759246145;
T636_W = 16384;
T637_W = -759222975;
T638_W = -1073741824;
T639_W = -759246145;
T640_W = 16384;
T641_W = -759222975;
T642_W = -1073741824;
T643_W = -759246145;
T644_W = 16384;
T645_W = -759222975;
T646_W = -1073741824;
T647_W = -759246145;
T648_W = 16384;
T649_W = -759222975;
T650_W = -1073741824;
T651_W = -759246145;
T652_W = 16384;
T653_W = -759222975;
T654_W = -1073741824;
T655_W = -759246145;
T656_W = 16384;
T657_W = -759222975;
T658_W = -1073741824;
T659_W = -759246145;
T660_W = 16384;
T661_W = -759222975;
T662_W = -1073741824;
T663_W = -759246145;
T664_W = 16384;
T665_W = -759222975;
T666_W = -1073741824;
T667_W = -759246145;
T668_W = 16384;
T669_W = -759222975;
T670_W = -1073741824;
T671_W = -759246145;
T672_W = 16384;
T673_W = -759222975;
T674_W = -1073741824;
T675_W = -759246145;
T676_W = 16384;
T677_W = -759222975;
T678_W = -1073741824;
T679_W = -759246145;
T680_W = 16384;
T681_W = -759222975;
T682_W = -1073741824;
T683_W = -759246145;
T684_W = 16384;
T685_W = -759222975;
T686_W = -1073741824;
T687_W = -759246145;
T688_W = 16384;
T689_W = -759222975;
T690_W = -1073741824;
T691_W = -759246145;
T692_W = 16384;
T693_W = -759222975;
T694_W = -1073741824;
T695_W = -759246145;
T696_W = 16384;
T697_W = -759222975;
T698_W = -1073741824;
T699_W = -759246145;
T700_W = 16384;
T701_W = -759222975;
T702_W = -1073741824;
T703_W = -759246145;
T704_W = 16384;
T705_W = -759222975;
T706_W = -1073741824;
T707_W = -759246145;
T708_W = 16384;
T709_W = -759222975;
T710_W = -1073741824;
T711_W = -759246145;
T712_W = 16384;
T713_W = -759222975;
T714_W = -1073741824;
T715_W = -759246145;
T716_W = 16384;
T717_W = -759222975;
T718_W = -1073741824;
T719_W = -759246145;
T720_W = 16384;
T721_W = -759222975;
T722_W = -1073741824;
T723_W = -759246145;
T724_W = 16384;
T725_W = -759222975;
T726_W = -1073741824;
T727_W = -759246145;
T728_W = 16384;
T729_W = -759222975;
T730_W = -1073741824;
T731_W = -759246145;
T732_W = 16384;
T733_W = -759222975;
T734_W = -1073741824;
T735_W = -759246145;
T736_W = 16384;
T737_W = -759222975;
T738_W = -1073741824;
T739_W = -759246145;
T740_W = 16384;
T741_W = -759222975;
T742_W = -1073741824;
T743_W = -759246145;
T744_W = 16384;
T745_W = -759222975;
T746_W = -1073741824;
T747_W = -759246145;
T748_W = 16384;
T749_W = -759222975;
T750_W = -1073741824;
T751_W = -759246145;
T752_W = 16384;
T753_W = -759222975;
T754_W = -1073741824;
T755_W = -759246145;
T756_W = 16384;
T757_W = -759222975;
T758_W = -1073741824;
T759_W = -759246145;
T760_W = 16384;
T761_W = -759222975;
T762_W = -1073741824;
T763_W = -759246145;
T764_W = 16384;
T765_W = -759222975;
T766_W = -1073741824;
T767_W = -759246145;

  // **** Code body **** //

	GET_FIFO(T512_i0, 0);
	GET_FIFO(T512_i1, 2);
	Butterfly(T512_i0, T512_i1, &T512_o0, &T512_o1, T512_W);
	PUT_FIFO(T512_o0, 0);
	PUT_FIFO(T512_o1, 1);

	GET_FIFO(T513_i0, 0);
	GET_FIFO(T513_i1, 2);
	Butterfly(T513_i0, T513_i1, &T513_o0, &T513_o1, T513_W);
	PUT_FIFO(T513_o0, 0);
	PUT_FIFO(T513_o1, 1);

	GET_FIFO(T514_i0, 1);
	GET_FIFO(T514_i1, 3);
	Butterfly(T514_i0, T514_i1, &T514_o0, &T514_o1, T514_W);
	PUT_FIFO(T514_o0, 0);
	PUT_FIFO(T514_o1, 1);

	GET_FIFO(T515_i0, 1);
	GET_FIFO(T515_i1, 3);
	Butterfly(T515_i0, T515_i1, &T515_o0, &T515_o1, T515_W);
	PUT_FIFO(T515_o0, 0);
	PUT_FIFO(T515_o1, 1);

	GET_FIFO(T516_i0, 0);
	GET_FIFO(T516_i1, 2);
	Butterfly(T516_i0, T516_i1, &T516_o0, &T516_o1, T516_W);
	PUT_FIFO(T516_o0, 2);
	PUT_FIFO(T516_o1, 3);

	GET_FIFO(T517_i0, 0);
	GET_FIFO(T517_i1, 2);
	Butterfly(T517_i0, T517_i1, &T517_o0, &T517_o1, T517_W);
	PUT_FIFO(T517_o0, 2);
	PUT_FIFO(T517_o1, 3);

	GET_FIFO(T518_i0, 1);
	GET_FIFO(T518_i1, 3);
	Butterfly(T518_i0, T518_i1, &T518_o0, &T518_o1, T518_W);
	PUT_FIFO(T518_o0, 2);
	PUT_FIFO(T518_o1, 3);

	GET_FIFO(T519_i0, 1);
	GET_FIFO(T519_i1, 3);
	Butterfly(T519_i0, T519_i1, &T519_o0, &T519_o1, T519_W);
	PUT_FIFO(T519_o0, 2);
	PUT_FIFO(T519_o1, 3);

	GET_FIFO(T520_i0, 0);
	GET_FIFO(T520_i1, 2);
	Butterfly(T520_i0, T520_i1, &T520_o0, &T520_o1, T520_W);
	PUT_FIFO(T520_o0, 0);
	PUT_FIFO(T520_o1, 1);

	GET_FIFO(T521_i0, 0);
	GET_FIFO(T521_i1, 2);
	Butterfly(T521_i0, T521_i1, &T521_o0, &T521_o1, T521_W);
	PUT_FIFO(T521_o0, 0);
	PUT_FIFO(T521_o1, 1);

	GET_FIFO(T522_i0, 1);
	GET_FIFO(T522_i1, 3);
	Butterfly(T522_i0, T522_i1, &T522_o0, &T522_o1, T522_W);
	PUT_FIFO(T522_o0, 0);
	PUT_FIFO(T522_o1, 1);

	GET_FIFO(T523_i0, 1);
	GET_FIFO(T523_i1, 3);
	Butterfly(T523_i0, T523_i1, &T523_o0, &T523_o1, T523_W);
	PUT_FIFO(T523_o0, 0);
	PUT_FIFO(T523_o1, 1);

	GET_FIFO(T524_i0, 0);
	GET_FIFO(T524_i1, 2);
	Butterfly(T524_i0, T524_i1, &T524_o0, &T524_o1, T524_W);
	PUT_FIFO(T524_o0, 2);
	PUT_FIFO(T524_o1, 3);

	GET_FIFO(T525_i0, 0);
	GET_FIFO(T525_i1, 2);
	Butterfly(T525_i0, T525_i1, &T525_o0, &T525_o1, T525_W);
	PUT_FIFO(T525_o0, 2);
	PUT_FIFO(T525_o1, 3);

	GET_FIFO(T526_i0, 1);
	GET_FIFO(T526_i1, 3);
	Butterfly(T526_i0, T526_i1, &T526_o0, &T526_o1, T526_W);
	PUT_FIFO(T526_o0, 2);
	PUT_FIFO(T526_o1, 3);

	GET_FIFO(T527_i0, 1);
	GET_FIFO(T527_i1, 3);
	Butterfly(T527_i0, T527_i1, &T527_o0, &T527_o1, T527_W);
	PUT_FIFO(T527_o0, 2);
	PUT_FIFO(T527_o1, 3);

	GET_FIFO(T528_i0, 0);
	GET_FIFO(T528_i1, 2);
	Butterfly(T528_i0, T528_i1, &T528_o0, &T528_o1, T528_W);
	PUT_FIFO(T528_o0, 0);
	PUT_FIFO(T528_o1, 1);

	GET_FIFO(T529_i0, 0);
	GET_FIFO(T529_i1, 2);
	Butterfly(T529_i0, T529_i1, &T529_o0, &T529_o1, T529_W);
	PUT_FIFO(T529_o0, 0);
	PUT_FIFO(T529_o1, 1);

	GET_FIFO(T530_i0, 1);
	GET_FIFO(T530_i1, 3);
	Butterfly(T530_i0, T530_i1, &T530_o0, &T530_o1, T530_W);
	PUT_FIFO(T530_o0, 0);
	PUT_FIFO(T530_o1, 1);

	GET_FIFO(T531_i0, 1);
	GET_FIFO(T531_i1, 3);
	Butterfly(T531_i0, T531_i1, &T531_o0, &T531_o1, T531_W);
	PUT_FIFO(T531_o0, 0);
	PUT_FIFO(T531_o1, 1);

	GET_FIFO(T532_i0, 0);
	GET_FIFO(T532_i1, 2);
	Butterfly(T532_i0, T532_i1, &T532_o0, &T532_o1, T532_W);
	PUT_FIFO(T532_o0, 2);
	PUT_FIFO(T532_o1, 3);

	GET_FIFO(T533_i0, 0);
	GET_FIFO(T533_i1, 2);
	Butterfly(T533_i0, T533_i1, &T533_o0, &T533_o1, T533_W);
	PUT_FIFO(T533_o0, 2);
	PUT_FIFO(T533_o1, 3);

	GET_FIFO(T534_i0, 1);
	GET_FIFO(T534_i1, 3);
	Butterfly(T534_i0, T534_i1, &T534_o0, &T534_o1, T534_W);
	PUT_FIFO(T534_o0, 2);
	PUT_FIFO(T534_o1, 3);

	GET_FIFO(T535_i0, 1);
	GET_FIFO(T535_i1, 3);
	Butterfly(T535_i0, T535_i1, &T535_o0, &T535_o1, T535_W);
	PUT_FIFO(T535_o0, 2);
	PUT_FIFO(T535_o1, 3);

	GET_FIFO(T536_i0, 0);
	GET_FIFO(T536_i1, 2);
	Butterfly(T536_i0, T536_i1, &T536_o0, &T536_o1, T536_W);
	PUT_FIFO(T536_o0, 0);
	PUT_FIFO(T536_o1, 1);

	GET_FIFO(T537_i0, 0);
	GET_FIFO(T537_i1, 2);
	Butterfly(T537_i0, T537_i1, &T537_o0, &T537_o1, T537_W);
	PUT_FIFO(T537_o0, 0);
	PUT_FIFO(T537_o1, 1);

	GET_FIFO(T538_i0, 1);
	GET_FIFO(T538_i1, 3);
	Butterfly(T538_i0, T538_i1, &T538_o0, &T538_o1, T538_W);
	PUT_FIFO(T538_o0, 0);
	PUT_FIFO(T538_o1, 1);

	GET_FIFO(T539_i0, 1);
	GET_FIFO(T539_i1, 3);
	Butterfly(T539_i0, T539_i1, &T539_o0, &T539_o1, T539_W);
	PUT_FIFO(T539_o0, 0);
	PUT_FIFO(T539_o1, 1);

	GET_FIFO(T540_i0, 0);
	GET_FIFO(T540_i1, 2);
	Butterfly(T540_i0, T540_i1, &T540_o0, &T540_o1, T540_W);
	PUT_FIFO(T540_o0, 2);
	PUT_FIFO(T540_o1, 3);

	GET_FIFO(T541_i0, 0);
	GET_FIFO(T541_i1, 2);
	Butterfly(T541_i0, T541_i1, &T541_o0, &T541_o1, T541_W);
	PUT_FIFO(T541_o0, 2);
	PUT_FIFO(T541_o1, 3);

	GET_FIFO(T542_i0, 1);
	GET_FIFO(T542_i1, 3);
	Butterfly(T542_i0, T542_i1, &T542_o0, &T542_o1, T542_W);
	PUT_FIFO(T542_o0, 2);
	PUT_FIFO(T542_o1, 3);

	GET_FIFO(T543_i0, 1);
	GET_FIFO(T543_i1, 3);
	Butterfly(T543_i0, T543_i1, &T543_o0, &T543_o1, T543_W);
	PUT_FIFO(T543_o0, 2);
	PUT_FIFO(T543_o1, 3);

	GET_FIFO(T544_i0, 0);
	GET_FIFO(T544_i1, 2);
	Butterfly(T544_i0, T544_i1, &T544_o0, &T544_o1, T544_W);
	PUT_FIFO(T544_o0, 0);
	PUT_FIFO(T544_o1, 1);

	GET_FIFO(T545_i0, 0);
	GET_FIFO(T545_i1, 2);
	Butterfly(T545_i0, T545_i1, &T545_o0, &T545_o1, T545_W);
	PUT_FIFO(T545_o0, 0);
	PUT_FIFO(T545_o1, 1);

	GET_FIFO(T546_i0, 1);
	GET_FIFO(T546_i1, 3);
	Butterfly(T546_i0, T546_i1, &T546_o0, &T546_o1, T546_W);
	PUT_FIFO(T546_o0, 0);
	PUT_FIFO(T546_o1, 1);

	GET_FIFO(T547_i0, 1);
	GET_FIFO(T547_i1, 3);
	Butterfly(T547_i0, T547_i1, &T547_o0, &T547_o1, T547_W);
	PUT_FIFO(T547_o0, 0);
	PUT_FIFO(T547_o1, 1);

	GET_FIFO(T548_i0, 0);
	GET_FIFO(T548_i1, 2);
	Butterfly(T548_i0, T548_i1, &T548_o0, &T548_o1, T548_W);
	PUT_FIFO(T548_o0, 2);
	PUT_FIFO(T548_o1, 3);

	GET_FIFO(T549_i0, 0);
	GET_FIFO(T549_i1, 2);
	Butterfly(T549_i0, T549_i1, &T549_o0, &T549_o1, T549_W);
	PUT_FIFO(T549_o0, 2);
	PUT_FIFO(T549_o1, 3);

	GET_FIFO(T550_i0, 1);
	GET_FIFO(T550_i1, 3);
	Butterfly(T550_i0, T550_i1, &T550_o0, &T550_o1, T550_W);
	PUT_FIFO(T550_o0, 2);
	PUT_FIFO(T550_o1, 3);

	GET_FIFO(T551_i0, 1);
	GET_FIFO(T551_i1, 3);
	Butterfly(T551_i0, T551_i1, &T551_o0, &T551_o1, T551_W);
	PUT_FIFO(T551_o0, 2);
	PUT_FIFO(T551_o1, 3);

	GET_FIFO(T552_i0, 0);
	GET_FIFO(T552_i1, 2);
	Butterfly(T552_i0, T552_i1, &T552_o0, &T552_o1, T552_W);
	PUT_FIFO(T552_o0, 0);
	PUT_FIFO(T552_o1, 1);

	GET_FIFO(T553_i0, 0);
	GET_FIFO(T553_i1, 2);
	Butterfly(T553_i0, T553_i1, &T553_o0, &T553_o1, T553_W);
	PUT_FIFO(T553_o0, 0);
	PUT_FIFO(T553_o1, 1);

	GET_FIFO(T554_i0, 1);
	GET_FIFO(T554_i1, 3);
	Butterfly(T554_i0, T554_i1, &T554_o0, &T554_o1, T554_W);
	PUT_FIFO(T554_o0, 0);
	PUT_FIFO(T554_o1, 1);

	GET_FIFO(T555_i0, 1);
	GET_FIFO(T555_i1, 3);
	Butterfly(T555_i0, T555_i1, &T555_o0, &T555_o1, T555_W);
	PUT_FIFO(T555_o0, 0);
	PUT_FIFO(T555_o1, 1);

	GET_FIFO(T556_i0, 0);
	GET_FIFO(T556_i1, 2);
	Butterfly(T556_i0, T556_i1, &T556_o0, &T556_o1, T556_W);
	PUT_FIFO(T556_o0, 2);
	PUT_FIFO(T556_o1, 3);

	GET_FIFO(T557_i0, 0);
	GET_FIFO(T557_i1, 2);
	Butterfly(T557_i0, T557_i1, &T557_o0, &T557_o1, T557_W);
	PUT_FIFO(T557_o0, 2);
	PUT_FIFO(T557_o1, 3);

	GET_FIFO(T558_i0, 1);
	GET_FIFO(T558_i1, 3);
	Butterfly(T558_i0, T558_i1, &T558_o0, &T558_o1, T558_W);
	PUT_FIFO(T558_o0, 2);
	PUT_FIFO(T558_o1, 3);

	GET_FIFO(T559_i0, 1);
	GET_FIFO(T559_i1, 3);
	Butterfly(T559_i0, T559_i1, &T559_o0, &T559_o1, T559_W);
	PUT_FIFO(T559_o0, 2);
	PUT_FIFO(T559_o1, 3);

	GET_FIFO(T560_i0, 0);
	GET_FIFO(T560_i1, 2);
	Butterfly(T560_i0, T560_i1, &T560_o0, &T560_o1, T560_W);
	PUT_FIFO(T560_o0, 0);
	PUT_FIFO(T560_o1, 1);

	GET_FIFO(T561_i0, 0);
	GET_FIFO(T561_i1, 2);
	Butterfly(T561_i0, T561_i1, &T561_o0, &T561_o1, T561_W);
	PUT_FIFO(T561_o0, 0);
	PUT_FIFO(T561_o1, 1);

	GET_FIFO(T562_i0, 1);
	GET_FIFO(T562_i1, 3);
	Butterfly(T562_i0, T562_i1, &T562_o0, &T562_o1, T562_W);
	PUT_FIFO(T562_o0, 0);
	PUT_FIFO(T562_o1, 1);

	GET_FIFO(T563_i0, 1);
	GET_FIFO(T563_i1, 3);
	Butterfly(T563_i0, T563_i1, &T563_o0, &T563_o1, T563_W);
	PUT_FIFO(T563_o0, 0);
	PUT_FIFO(T563_o1, 1);

	GET_FIFO(T564_i0, 0);
	GET_FIFO(T564_i1, 2);
	Butterfly(T564_i0, T564_i1, &T564_o0, &T564_o1, T564_W);
	PUT_FIFO(T564_o0, 2);
	PUT_FIFO(T564_o1, 3);

	GET_FIFO(T565_i0, 0);
	GET_FIFO(T565_i1, 2);
	Butterfly(T565_i0, T565_i1, &T565_o0, &T565_o1, T565_W);
	PUT_FIFO(T565_o0, 2);
	PUT_FIFO(T565_o1, 3);

	GET_FIFO(T566_i0, 1);
	GET_FIFO(T566_i1, 3);
	Butterfly(T566_i0, T566_i1, &T566_o0, &T566_o1, T566_W);
	PUT_FIFO(T566_o0, 2);
	PUT_FIFO(T566_o1, 3);

	GET_FIFO(T567_i0, 1);
	GET_FIFO(T567_i1, 3);
	Butterfly(T567_i0, T567_i1, &T567_o0, &T567_o1, T567_W);
	PUT_FIFO(T567_o0, 2);
	PUT_FIFO(T567_o1, 3);

	GET_FIFO(T568_i0, 0);
	GET_FIFO(T568_i1, 2);
	Butterfly(T568_i0, T568_i1, &T568_o0, &T568_o1, T568_W);
	PUT_FIFO(T568_o0, 0);
	PUT_FIFO(T568_o1, 1);

	GET_FIFO(T569_i0, 0);
	GET_FIFO(T569_i1, 2);
	Butterfly(T569_i0, T569_i1, &T569_o0, &T569_o1, T569_W);
	PUT_FIFO(T569_o0, 0);
	PUT_FIFO(T569_o1, 1);

	GET_FIFO(T570_i0, 1);
	GET_FIFO(T570_i1, 3);
	Butterfly(T570_i0, T570_i1, &T570_o0, &T570_o1, T570_W);
	PUT_FIFO(T570_o0, 0);
	PUT_FIFO(T570_o1, 1);

	GET_FIFO(T571_i0, 1);
	GET_FIFO(T571_i1, 3);
	Butterfly(T571_i0, T571_i1, &T571_o0, &T571_o1, T571_W);
	PUT_FIFO(T571_o0, 0);
	PUT_FIFO(T571_o1, 1);

	GET_FIFO(T572_i0, 0);
	GET_FIFO(T572_i1, 2);
	Butterfly(T572_i0, T572_i1, &T572_o0, &T572_o1, T572_W);
	PUT_FIFO(T572_o0, 2);
	PUT_FIFO(T572_o1, 3);

	GET_FIFO(T573_i0, 0);
	GET_FIFO(T573_i1, 2);
	Butterfly(T573_i0, T573_i1, &T573_o0, &T573_o1, T573_W);
	PUT_FIFO(T573_o0, 2);
	PUT_FIFO(T573_o1, 3);

	GET_FIFO(T574_i0, 1);
	GET_FIFO(T574_i1, 3);
	Butterfly(T574_i0, T574_i1, &T574_o0, &T574_o1, T574_W);
	PUT_FIFO(T574_o0, 2);
	PUT_FIFO(T574_o1, 3);

	GET_FIFO(T575_i0, 1);
	GET_FIFO(T575_i1, 3);
	Butterfly(T575_i0, T575_i1, &T575_o0, &T575_o1, T575_W);
	PUT_FIFO(T575_o0, 2);
	PUT_FIFO(T575_o1, 3);

	GET_FIFO(T576_i0, 0);
	GET_FIFO(T576_i1, 2);
	Butterfly(T576_i0, T576_i1, &T576_o0, &T576_o1, T576_W);
	PUT_FIFO(T576_o0, 0);
	PUT_FIFO(T576_o1, 1);

	GET_FIFO(T577_i0, 0);
	GET_FIFO(T577_i1, 2);
	Butterfly(T577_i0, T577_i1, &T577_o0, &T577_o1, T577_W);
	PUT_FIFO(T577_o0, 0);
	PUT_FIFO(T577_o1, 1);

	GET_FIFO(T578_i0, 1);
	GET_FIFO(T578_i1, 3);
	Butterfly(T578_i0, T578_i1, &T578_o0, &T578_o1, T578_W);
	PUT_FIFO(T578_o0, 0);
	PUT_FIFO(T578_o1, 1);

	GET_FIFO(T579_i0, 1);
	GET_FIFO(T579_i1, 3);
	Butterfly(T579_i0, T579_i1, &T579_o0, &T579_o1, T579_W);
	PUT_FIFO(T579_o0, 0);
	PUT_FIFO(T579_o1, 1);

	GET_FIFO(T580_i0, 0);
	GET_FIFO(T580_i1, 2);
	Butterfly(T580_i0, T580_i1, &T580_o0, &T580_o1, T580_W);
	PUT_FIFO(T580_o0, 2);
	PUT_FIFO(T580_o1, 3);

	GET_FIFO(T581_i0, 0);
	GET_FIFO(T581_i1, 2);
	Butterfly(T581_i0, T581_i1, &T581_o0, &T581_o1, T581_W);
	PUT_FIFO(T581_o0, 2);
	PUT_FIFO(T581_o1, 3);

	GET_FIFO(T582_i0, 1);
	GET_FIFO(T582_i1, 3);
	Butterfly(T582_i0, T582_i1, &T582_o0, &T582_o1, T582_W);
	PUT_FIFO(T582_o0, 2);
	PUT_FIFO(T582_o1, 3);

	GET_FIFO(T583_i0, 1);
	GET_FIFO(T583_i1, 3);
	Butterfly(T583_i0, T583_i1, &T583_o0, &T583_o1, T583_W);
	PUT_FIFO(T583_o0, 2);
	PUT_FIFO(T583_o1, 3);

	GET_FIFO(T584_i0, 0);
	GET_FIFO(T584_i1, 2);
	Butterfly(T584_i0, T584_i1, &T584_o0, &T584_o1, T584_W);
	PUT_FIFO(T584_o0, 0);
	PUT_FIFO(T584_o1, 1);

	GET_FIFO(T585_i0, 0);
	GET_FIFO(T585_i1, 2);
	Butterfly(T585_i0, T585_i1, &T585_o0, &T585_o1, T585_W);
	PUT_FIFO(T585_o0, 0);
	PUT_FIFO(T585_o1, 1);

	GET_FIFO(T586_i0, 1);
	GET_FIFO(T586_i1, 3);
	Butterfly(T586_i0, T586_i1, &T586_o0, &T586_o1, T586_W);
	PUT_FIFO(T586_o0, 0);
	PUT_FIFO(T586_o1, 1);

	GET_FIFO(T587_i0, 1);
	GET_FIFO(T587_i1, 3);
	Butterfly(T587_i0, T587_i1, &T587_o0, &T587_o1, T587_W);
	PUT_FIFO(T587_o0, 0);
	PUT_FIFO(T587_o1, 1);

	GET_FIFO(T588_i0, 0);
	GET_FIFO(T588_i1, 2);
	Butterfly(T588_i0, T588_i1, &T588_o0, &T588_o1, T588_W);
	PUT_FIFO(T588_o0, 2);
	PUT_FIFO(T588_o1, 3);

	GET_FIFO(T589_i0, 0);
	GET_FIFO(T589_i1, 2);
	Butterfly(T589_i0, T589_i1, &T589_o0, &T589_o1, T589_W);
	PUT_FIFO(T589_o0, 2);
	PUT_FIFO(T589_o1, 3);

	GET_FIFO(T590_i0, 1);
	GET_FIFO(T590_i1, 3);
	Butterfly(T590_i0, T590_i1, &T590_o0, &T590_o1, T590_W);
	PUT_FIFO(T590_o0, 2);
	PUT_FIFO(T590_o1, 3);

	GET_FIFO(T591_i0, 1);
	GET_FIFO(T591_i1, 3);
	Butterfly(T591_i0, T591_i1, &T591_o0, &T591_o1, T591_W);
	PUT_FIFO(T591_o0, 2);
	PUT_FIFO(T591_o1, 3);

	GET_FIFO(T592_i0, 0);
	GET_FIFO(T592_i1, 2);
	Butterfly(T592_i0, T592_i1, &T592_o0, &T592_o1, T592_W);
	PUT_FIFO(T592_o0, 0);
	PUT_FIFO(T592_o1, 1);

	GET_FIFO(T593_i0, 0);
	GET_FIFO(T593_i1, 2);
	Butterfly(T593_i0, T593_i1, &T593_o0, &T593_o1, T593_W);
	PUT_FIFO(T593_o0, 0);
	PUT_FIFO(T593_o1, 1);

	GET_FIFO(T594_i0, 1);
	GET_FIFO(T594_i1, 3);
	Butterfly(T594_i0, T594_i1, &T594_o0, &T594_o1, T594_W);
	PUT_FIFO(T594_o0, 0);
	PUT_FIFO(T594_o1, 1);

	GET_FIFO(T595_i0, 1);
	GET_FIFO(T595_i1, 3);
	Butterfly(T595_i0, T595_i1, &T595_o0, &T595_o1, T595_W);
	PUT_FIFO(T595_o0, 0);
	PUT_FIFO(T595_o1, 1);

	GET_FIFO(T596_i0, 0);
	GET_FIFO(T596_i1, 2);
	Butterfly(T596_i0, T596_i1, &T596_o0, &T596_o1, T596_W);
	PUT_FIFO(T596_o0, 2);
	PUT_FIFO(T596_o1, 3);

	GET_FIFO(T597_i0, 0);
	GET_FIFO(T597_i1, 2);
	Butterfly(T597_i0, T597_i1, &T597_o0, &T597_o1, T597_W);
	PUT_FIFO(T597_o0, 2);
	PUT_FIFO(T597_o1, 3);

	GET_FIFO(T598_i0, 1);
	GET_FIFO(T598_i1, 3);
	Butterfly(T598_i0, T598_i1, &T598_o0, &T598_o1, T598_W);
	PUT_FIFO(T598_o0, 2);
	PUT_FIFO(T598_o1, 3);

	GET_FIFO(T599_i0, 1);
	GET_FIFO(T599_i1, 3);
	Butterfly(T599_i0, T599_i1, &T599_o0, &T599_o1, T599_W);
	PUT_FIFO(T599_o0, 2);
	PUT_FIFO(T599_o1, 3);

	GET_FIFO(T600_i0, 0);
	GET_FIFO(T600_i1, 2);
	Butterfly(T600_i0, T600_i1, &T600_o0, &T600_o1, T600_W);
	PUT_FIFO(T600_o0, 0);
	PUT_FIFO(T600_o1, 1);

	GET_FIFO(T601_i0, 0);
	GET_FIFO(T601_i1, 2);
	Butterfly(T601_i0, T601_i1, &T601_o0, &T601_o1, T601_W);
	PUT_FIFO(T601_o0, 0);
	PUT_FIFO(T601_o1, 1);

	GET_FIFO(T602_i0, 1);
	GET_FIFO(T602_i1, 3);
	Butterfly(T602_i0, T602_i1, &T602_o0, &T602_o1, T602_W);
	PUT_FIFO(T602_o0, 0);
	PUT_FIFO(T602_o1, 1);

	GET_FIFO(T603_i0, 1);
	GET_FIFO(T603_i1, 3);
	Butterfly(T603_i0, T603_i1, &T603_o0, &T603_o1, T603_W);
	PUT_FIFO(T603_o0, 0);
	PUT_FIFO(T603_o1, 1);

	GET_FIFO(T604_i0, 0);
	GET_FIFO(T604_i1, 2);
	Butterfly(T604_i0, T604_i1, &T604_o0, &T604_o1, T604_W);
	PUT_FIFO(T604_o0, 2);
	PUT_FIFO(T604_o1, 3);

	GET_FIFO(T605_i0, 0);
	GET_FIFO(T605_i1, 2);
	Butterfly(T605_i0, T605_i1, &T605_o0, &T605_o1, T605_W);
	PUT_FIFO(T605_o0, 2);
	PUT_FIFO(T605_o1, 3);

	GET_FIFO(T606_i0, 1);
	GET_FIFO(T606_i1, 3);
	Butterfly(T606_i0, T606_i1, &T606_o0, &T606_o1, T606_W);
	PUT_FIFO(T606_o0, 2);
	PUT_FIFO(T606_o1, 3);

	GET_FIFO(T607_i0, 1);
	GET_FIFO(T607_i1, 3);
	Butterfly(T607_i0, T607_i1, &T607_o0, &T607_o1, T607_W);
	PUT_FIFO(T607_o0, 2);
	PUT_FIFO(T607_o1, 3);

	GET_FIFO(T608_i0, 0);
	GET_FIFO(T608_i1, 2);
	Butterfly(T608_i0, T608_i1, &T608_o0, &T608_o1, T608_W);
	PUT_FIFO(T608_o0, 0);
	PUT_FIFO(T608_o1, 1);

	GET_FIFO(T609_i0, 0);
	GET_FIFO(T609_i1, 2);
	Butterfly(T609_i0, T609_i1, &T609_o0, &T609_o1, T609_W);
	PUT_FIFO(T609_o0, 0);
	PUT_FIFO(T609_o1, 1);

	GET_FIFO(T610_i0, 1);
	GET_FIFO(T610_i1, 3);
	Butterfly(T610_i0, T610_i1, &T610_o0, &T610_o1, T610_W);
	PUT_FIFO(T610_o0, 0);
	PUT_FIFO(T610_o1, 1);

	GET_FIFO(T611_i0, 1);
	GET_FIFO(T611_i1, 3);
	Butterfly(T611_i0, T611_i1, &T611_o0, &T611_o1, T611_W);
	PUT_FIFO(T611_o0, 0);
	PUT_FIFO(T611_o1, 1);

	GET_FIFO(T612_i0, 0);
	GET_FIFO(T612_i1, 2);
	Butterfly(T612_i0, T612_i1, &T612_o0, &T612_o1, T612_W);
	PUT_FIFO(T612_o0, 2);
	PUT_FIFO(T612_o1, 3);

	GET_FIFO(T613_i0, 0);
	GET_FIFO(T613_i1, 2);
	Butterfly(T613_i0, T613_i1, &T613_o0, &T613_o1, T613_W);
	PUT_FIFO(T613_o0, 2);
	PUT_FIFO(T613_o1, 3);

	GET_FIFO(T614_i0, 1);
	GET_FIFO(T614_i1, 3);
	Butterfly(T614_i0, T614_i1, &T614_o0, &T614_o1, T614_W);
	PUT_FIFO(T614_o0, 2);
	PUT_FIFO(T614_o1, 3);

	GET_FIFO(T615_i0, 1);
	GET_FIFO(T615_i1, 3);
	Butterfly(T615_i0, T615_i1, &T615_o0, &T615_o1, T615_W);
	PUT_FIFO(T615_o0, 2);
	PUT_FIFO(T615_o1, 3);

	GET_FIFO(T616_i0, 0);
	GET_FIFO(T616_i1, 2);
	Butterfly(T616_i0, T616_i1, &T616_o0, &T616_o1, T616_W);
	PUT_FIFO(T616_o0, 0);
	PUT_FIFO(T616_o1, 1);

	GET_FIFO(T617_i0, 0);
	GET_FIFO(T617_i1, 2);
	Butterfly(T617_i0, T617_i1, &T617_o0, &T617_o1, T617_W);
	PUT_FIFO(T617_o0, 0);
	PUT_FIFO(T617_o1, 1);

	GET_FIFO(T618_i0, 1);
	GET_FIFO(T618_i1, 3);
	Butterfly(T618_i0, T618_i1, &T618_o0, &T618_o1, T618_W);
	PUT_FIFO(T618_o0, 0);
	PUT_FIFO(T618_o1, 1);

	GET_FIFO(T619_i0, 1);
	GET_FIFO(T619_i1, 3);
	Butterfly(T619_i0, T619_i1, &T619_o0, &T619_o1, T619_W);
	PUT_FIFO(T619_o0, 0);
	PUT_FIFO(T619_o1, 1);

	GET_FIFO(T620_i0, 0);
	GET_FIFO(T620_i1, 2);
	Butterfly(T620_i0, T620_i1, &T620_o0, &T620_o1, T620_W);
	PUT_FIFO(T620_o0, 2);
	PUT_FIFO(T620_o1, 3);

	GET_FIFO(T621_i0, 0);
	GET_FIFO(T621_i1, 2);
	Butterfly(T621_i0, T621_i1, &T621_o0, &T621_o1, T621_W);
	PUT_FIFO(T621_o0, 2);
	PUT_FIFO(T621_o1, 3);

	GET_FIFO(T622_i0, 1);
	GET_FIFO(T622_i1, 3);
	Butterfly(T622_i0, T622_i1, &T622_o0, &T622_o1, T622_W);
	PUT_FIFO(T622_o0, 2);
	PUT_FIFO(T622_o1, 3);

	GET_FIFO(T623_i0, 1);
	GET_FIFO(T623_i1, 3);
	Butterfly(T623_i0, T623_i1, &T623_o0, &T623_o1, T623_W);
	PUT_FIFO(T623_o0, 2);
	PUT_FIFO(T623_o1, 3);

	GET_FIFO(T624_i0, 0);
	GET_FIFO(T624_i1, 2);
	Butterfly(T624_i0, T624_i1, &T624_o0, &T624_o1, T624_W);
	PUT_FIFO(T624_o0, 0);
	PUT_FIFO(T624_o1, 1);

	GET_FIFO(T625_i0, 0);
	GET_FIFO(T625_i1, 2);
	Butterfly(T625_i0, T625_i1, &T625_o0, &T625_o1, T625_W);
	PUT_FIFO(T625_o0, 0);
	PUT_FIFO(T625_o1, 1);

	GET_FIFO(T626_i0, 1);
	GET_FIFO(T626_i1, 3);
	Butterfly(T626_i0, T626_i1, &T626_o0, &T626_o1, T626_W);
	PUT_FIFO(T626_o0, 0);
	PUT_FIFO(T626_o1, 1);

	GET_FIFO(T627_i0, 1);
	GET_FIFO(T627_i1, 3);
	Butterfly(T627_i0, T627_i1, &T627_o0, &T627_o1, T627_W);
	PUT_FIFO(T627_o0, 0);
	PUT_FIFO(T627_o1, 1);

	GET_FIFO(T628_i0, 0);
	GET_FIFO(T628_i1, 2);
	Butterfly(T628_i0, T628_i1, &T628_o0, &T628_o1, T628_W);
	PUT_FIFO(T628_o0, 2);
	PUT_FIFO(T628_o1, 3);

	GET_FIFO(T629_i0, 0);
	GET_FIFO(T629_i1, 2);
	Butterfly(T629_i0, T629_i1, &T629_o0, &T629_o1, T629_W);
	PUT_FIFO(T629_o0, 2);
	PUT_FIFO(T629_o1, 3);

	GET_FIFO(T630_i0, 1);
	GET_FIFO(T630_i1, 3);
	Butterfly(T630_i0, T630_i1, &T630_o0, &T630_o1, T630_W);
	PUT_FIFO(T630_o0, 2);
	PUT_FIFO(T630_o1, 3);

	GET_FIFO(T631_i0, 1);
	GET_FIFO(T631_i1, 3);
	Butterfly(T631_i0, T631_i1, &T631_o0, &T631_o1, T631_W);
	PUT_FIFO(T631_o0, 2);
	PUT_FIFO(T631_o1, 3);

	GET_FIFO(T632_i0, 0);
	GET_FIFO(T632_i1, 2);
	Butterfly(T632_i0, T632_i1, &T632_o0, &T632_o1, T632_W);
	PUT_FIFO(T632_o0, 0);
	PUT_FIFO(T632_o1, 1);

	GET_FIFO(T633_i0, 0);
	GET_FIFO(T633_i1, 2);
	Butterfly(T633_i0, T633_i1, &T633_o0, &T633_o1, T633_W);
	PUT_FIFO(T633_o0, 0);
	PUT_FIFO(T633_o1, 1);

	GET_FIFO(T634_i0, 1);
	GET_FIFO(T634_i1, 3);
	Butterfly(T634_i0, T634_i1, &T634_o0, &T634_o1, T634_W);
	PUT_FIFO(T634_o0, 0);
	PUT_FIFO(T634_o1, 1);

	GET_FIFO(T635_i0, 1);
	GET_FIFO(T635_i1, 3);
	Butterfly(T635_i0, T635_i1, &T635_o0, &T635_o1, T635_W);
	PUT_FIFO(T635_o0, 0);
	PUT_FIFO(T635_o1, 1);

	GET_FIFO(T636_i0, 0);
	GET_FIFO(T636_i1, 2);
	Butterfly(T636_i0, T636_i1, &T636_o0, &T636_o1, T636_W);
	PUT_FIFO(T636_o0, 2);
	PUT_FIFO(T636_o1, 3);

	GET_FIFO(T637_i0, 0);
	GET_FIFO(T637_i1, 2);
	Butterfly(T637_i0, T637_i1, &T637_o0, &T637_o1, T637_W);
	PUT_FIFO(T637_o0, 2);
	PUT_FIFO(T637_o1, 3);

	GET_FIFO(T638_i0, 1);
	GET_FIFO(T638_i1, 3);
	Butterfly(T638_i0, T638_i1, &T638_o0, &T638_o1, T638_W);
	PUT_FIFO(T638_o0, 2);
	PUT_FIFO(T638_o1, 3);

	GET_FIFO(T639_i0, 1);
	GET_FIFO(T639_i1, 3);
	Butterfly(T639_i0, T639_i1, &T639_o0, &T639_o1, T639_W);
	PUT_FIFO(T639_o0, 2);
	PUT_FIFO(T639_o1, 3);

	GET_FIFO(T640_i0, 0);
	GET_FIFO(T640_i1, 2);
	Butterfly(T640_i0, T640_i1, &T640_o0, &T640_o1, T640_W);
	PUT_FIFO(T640_o0, 0);
	PUT_FIFO(T640_o1, 1);

	GET_FIFO(T641_i0, 0);
	GET_FIFO(T641_i1, 2);
	Butterfly(T641_i0, T641_i1, &T641_o0, &T641_o1, T641_W);
	PUT_FIFO(T641_o0, 0);
	PUT_FIFO(T641_o1, 1);

	GET_FIFO(T642_i0, 1);
	GET_FIFO(T642_i1, 3);
	Butterfly(T642_i0, T642_i1, &T642_o0, &T642_o1, T642_W);
	PUT_FIFO(T642_o0, 0);
	PUT_FIFO(T642_o1, 1);

	GET_FIFO(T643_i0, 1);
	GET_FIFO(T643_i1, 3);
	Butterfly(T643_i0, T643_i1, &T643_o0, &T643_o1, T643_W);
	PUT_FIFO(T643_o0, 0);
	PUT_FIFO(T643_o1, 1);

	GET_FIFO(T644_i0, 0);
	GET_FIFO(T644_i1, 2);
	Butterfly(T644_i0, T644_i1, &T644_o0, &T644_o1, T644_W);
	PUT_FIFO(T644_o0, 2);
	PUT_FIFO(T644_o1, 3);

	GET_FIFO(T645_i0, 0);
	GET_FIFO(T645_i1, 2);
	Butterfly(T645_i0, T645_i1, &T645_o0, &T645_o1, T645_W);
	PUT_FIFO(T645_o0, 2);
	PUT_FIFO(T645_o1, 3);

	GET_FIFO(T646_i0, 1);
	GET_FIFO(T646_i1, 3);
	Butterfly(T646_i0, T646_i1, &T646_o0, &T646_o1, T646_W);
	PUT_FIFO(T646_o0, 2);
	PUT_FIFO(T646_o1, 3);

	GET_FIFO(T647_i0, 1);
	GET_FIFO(T647_i1, 3);
	Butterfly(T647_i0, T647_i1, &T647_o0, &T647_o1, T647_W);
	PUT_FIFO(T647_o0, 2);
	PUT_FIFO(T647_o1, 3);

	GET_FIFO(T648_i0, 0);
	GET_FIFO(T648_i1, 2);
	Butterfly(T648_i0, T648_i1, &T648_o0, &T648_o1, T648_W);
	PUT_FIFO(T648_o0, 0);
	PUT_FIFO(T648_o1, 1);

	GET_FIFO(T649_i0, 0);
	GET_FIFO(T649_i1, 2);
	Butterfly(T649_i0, T649_i1, &T649_o0, &T649_o1, T649_W);
	PUT_FIFO(T649_o0, 0);
	PUT_FIFO(T649_o1, 1);

	GET_FIFO(T650_i0, 1);
	GET_FIFO(T650_i1, 3);
	Butterfly(T650_i0, T650_i1, &T650_o0, &T650_o1, T650_W);
	PUT_FIFO(T650_o0, 0);
	PUT_FIFO(T650_o1, 1);

	GET_FIFO(T651_i0, 1);
	GET_FIFO(T651_i1, 3);
	Butterfly(T651_i0, T651_i1, &T651_o0, &T651_o1, T651_W);
	PUT_FIFO(T651_o0, 0);
	PUT_FIFO(T651_o1, 1);

	GET_FIFO(T652_i0, 0);
	GET_FIFO(T652_i1, 2);
	Butterfly(T652_i0, T652_i1, &T652_o0, &T652_o1, T652_W);
	PUT_FIFO(T652_o0, 2);
	PUT_FIFO(T652_o1, 3);

	GET_FIFO(T653_i0, 0);
	GET_FIFO(T653_i1, 2);
	Butterfly(T653_i0, T653_i1, &T653_o0, &T653_o1, T653_W);
	PUT_FIFO(T653_o0, 2);
	PUT_FIFO(T653_o1, 3);

	GET_FIFO(T654_i0, 1);
	GET_FIFO(T654_i1, 3);
	Butterfly(T654_i0, T654_i1, &T654_o0, &T654_o1, T654_W);
	PUT_FIFO(T654_o0, 2);
	PUT_FIFO(T654_o1, 3);

	GET_FIFO(T655_i0, 1);
	GET_FIFO(T655_i1, 3);
	Butterfly(T655_i0, T655_i1, &T655_o0, &T655_o1, T655_W);
	PUT_FIFO(T655_o0, 2);
	PUT_FIFO(T655_o1, 3);

	GET_FIFO(T656_i0, 0);
	GET_FIFO(T656_i1, 2);
	Butterfly(T656_i0, T656_i1, &T656_o0, &T656_o1, T656_W);
	PUT_FIFO(T656_o0, 0);
	PUT_FIFO(T656_o1, 1);

	GET_FIFO(T657_i0, 0);
	GET_FIFO(T657_i1, 2);
	Butterfly(T657_i0, T657_i1, &T657_o0, &T657_o1, T657_W);
	PUT_FIFO(T657_o0, 0);
	PUT_FIFO(T657_o1, 1);

	GET_FIFO(T658_i0, 1);
	GET_FIFO(T658_i1, 3);
	Butterfly(T658_i0, T658_i1, &T658_o0, &T658_o1, T658_W);
	PUT_FIFO(T658_o0, 0);
	PUT_FIFO(T658_o1, 1);

	GET_FIFO(T659_i0, 1);
	GET_FIFO(T659_i1, 3);
	Butterfly(T659_i0, T659_i1, &T659_o0, &T659_o1, T659_W);
	PUT_FIFO(T659_o0, 0);
	PUT_FIFO(T659_o1, 1);

	GET_FIFO(T660_i0, 0);
	GET_FIFO(T660_i1, 2);
	Butterfly(T660_i0, T660_i1, &T660_o0, &T660_o1, T660_W);
	PUT_FIFO(T660_o0, 2);
	PUT_FIFO(T660_o1, 3);

	GET_FIFO(T661_i0, 0);
	GET_FIFO(T661_i1, 2);
	Butterfly(T661_i0, T661_i1, &T661_o0, &T661_o1, T661_W);
	PUT_FIFO(T661_o0, 2);
	PUT_FIFO(T661_o1, 3);

	GET_FIFO(T662_i0, 1);
	GET_FIFO(T662_i1, 3);
	Butterfly(T662_i0, T662_i1, &T662_o0, &T662_o1, T662_W);
	PUT_FIFO(T662_o0, 2);
	PUT_FIFO(T662_o1, 3);

	GET_FIFO(T663_i0, 1);
	GET_FIFO(T663_i1, 3);
	Butterfly(T663_i0, T663_i1, &T663_o0, &T663_o1, T663_W);
	PUT_FIFO(T663_o0, 2);
	PUT_FIFO(T663_o1, 3);

	GET_FIFO(T664_i0, 0);
	GET_FIFO(T664_i1, 2);
	Butterfly(T664_i0, T664_i1, &T664_o0, &T664_o1, T664_W);
	PUT_FIFO(T664_o0, 0);
	PUT_FIFO(T664_o1, 1);

	GET_FIFO(T665_i0, 0);
	GET_FIFO(T665_i1, 2);
	Butterfly(T665_i0, T665_i1, &T665_o0, &T665_o1, T665_W);
	PUT_FIFO(T665_o0, 0);
	PUT_FIFO(T665_o1, 1);

	GET_FIFO(T666_i0, 1);
	GET_FIFO(T666_i1, 3);
	Butterfly(T666_i0, T666_i1, &T666_o0, &T666_o1, T666_W);
	PUT_FIFO(T666_o0, 0);
	PUT_FIFO(T666_o1, 1);

	GET_FIFO(T667_i0, 1);
	GET_FIFO(T667_i1, 3);
	Butterfly(T667_i0, T667_i1, &T667_o0, &T667_o1, T667_W);
	PUT_FIFO(T667_o0, 0);
	PUT_FIFO(T667_o1, 1);

	GET_FIFO(T668_i0, 0);
	GET_FIFO(T668_i1, 2);
	Butterfly(T668_i0, T668_i1, &T668_o0, &T668_o1, T668_W);
	PUT_FIFO(T668_o0, 2);
	PUT_FIFO(T668_o1, 3);

	GET_FIFO(T669_i0, 0);
	GET_FIFO(T669_i1, 2);
	Butterfly(T669_i0, T669_i1, &T669_o0, &T669_o1, T669_W);
	PUT_FIFO(T669_o0, 2);
	PUT_FIFO(T669_o1, 3);

	GET_FIFO(T670_i0, 1);
	GET_FIFO(T670_i1, 3);
	Butterfly(T670_i0, T670_i1, &T670_o0, &T670_o1, T670_W);
	PUT_FIFO(T670_o0, 2);
	PUT_FIFO(T670_o1, 3);

	GET_FIFO(T671_i0, 1);
	GET_FIFO(T671_i1, 3);
	Butterfly(T671_i0, T671_i1, &T671_o0, &T671_o1, T671_W);
	PUT_FIFO(T671_o0, 2);
	PUT_FIFO(T671_o1, 3);

	GET_FIFO(T672_i0, 0);
	GET_FIFO(T672_i1, 2);
	Butterfly(T672_i0, T672_i1, &T672_o0, &T672_o1, T672_W);
	PUT_FIFO(T672_o0, 0);
	PUT_FIFO(T672_o1, 1);

	GET_FIFO(T673_i0, 0);
	GET_FIFO(T673_i1, 2);
	Butterfly(T673_i0, T673_i1, &T673_o0, &T673_o1, T673_W);
	PUT_FIFO(T673_o0, 0);
	PUT_FIFO(T673_o1, 1);

	GET_FIFO(T674_i0, 1);
	GET_FIFO(T674_i1, 3);
	Butterfly(T674_i0, T674_i1, &T674_o0, &T674_o1, T674_W);
	PUT_FIFO(T674_o0, 0);
	PUT_FIFO(T674_o1, 1);

	GET_FIFO(T675_i0, 1);
	GET_FIFO(T675_i1, 3);
	Butterfly(T675_i0, T675_i1, &T675_o0, &T675_o1, T675_W);
	PUT_FIFO(T675_o0, 0);
	PUT_FIFO(T675_o1, 1);

	GET_FIFO(T676_i0, 0);
	GET_FIFO(T676_i1, 2);
	Butterfly(T676_i0, T676_i1, &T676_o0, &T676_o1, T676_W);
	PUT_FIFO(T676_o0, 2);
	PUT_FIFO(T676_o1, 3);

	GET_FIFO(T677_i0, 0);
	GET_FIFO(T677_i1, 2);
	Butterfly(T677_i0, T677_i1, &T677_o0, &T677_o1, T677_W);
	PUT_FIFO(T677_o0, 2);
	PUT_FIFO(T677_o1, 3);

	GET_FIFO(T678_i0, 1);
	GET_FIFO(T678_i1, 3);
	Butterfly(T678_i0, T678_i1, &T678_o0, &T678_o1, T678_W);
	PUT_FIFO(T678_o0, 2);
	PUT_FIFO(T678_o1, 3);

	GET_FIFO(T679_i0, 1);
	GET_FIFO(T679_i1, 3);
	Butterfly(T679_i0, T679_i1, &T679_o0, &T679_o1, T679_W);
	PUT_FIFO(T679_o0, 2);
	PUT_FIFO(T679_o1, 3);

	GET_FIFO(T680_i0, 0);
	GET_FIFO(T680_i1, 2);
	Butterfly(T680_i0, T680_i1, &T680_o0, &T680_o1, T680_W);
	PUT_FIFO(T680_o0, 0);
	PUT_FIFO(T680_o1, 1);

	GET_FIFO(T681_i0, 0);
	GET_FIFO(T681_i1, 2);
	Butterfly(T681_i0, T681_i1, &T681_o0, &T681_o1, T681_W);
	PUT_FIFO(T681_o0, 0);
	PUT_FIFO(T681_o1, 1);

	GET_FIFO(T682_i0, 1);
	GET_FIFO(T682_i1, 3);
	Butterfly(T682_i0, T682_i1, &T682_o0, &T682_o1, T682_W);
	PUT_FIFO(T682_o0, 0);
	PUT_FIFO(T682_o1, 1);

	GET_FIFO(T683_i0, 1);
	GET_FIFO(T683_i1, 3);
	Butterfly(T683_i0, T683_i1, &T683_o0, &T683_o1, T683_W);
	PUT_FIFO(T683_o0, 0);
	PUT_FIFO(T683_o1, 1);

	GET_FIFO(T684_i0, 0);
	GET_FIFO(T684_i1, 2);
	Butterfly(T684_i0, T684_i1, &T684_o0, &T684_o1, T684_W);
	PUT_FIFO(T684_o0, 2);
	PUT_FIFO(T684_o1, 3);

	GET_FIFO(T685_i0, 0);
	GET_FIFO(T685_i1, 2);
	Butterfly(T685_i0, T685_i1, &T685_o0, &T685_o1, T685_W);
	PUT_FIFO(T685_o0, 2);
	PUT_FIFO(T685_o1, 3);

	GET_FIFO(T686_i0, 1);
	GET_FIFO(T686_i1, 3);
	Butterfly(T686_i0, T686_i1, &T686_o0, &T686_o1, T686_W);
	PUT_FIFO(T686_o0, 2);
	PUT_FIFO(T686_o1, 3);

	GET_FIFO(T687_i0, 1);
	GET_FIFO(T687_i1, 3);
	Butterfly(T687_i0, T687_i1, &T687_o0, &T687_o1, T687_W);
	PUT_FIFO(T687_o0, 2);
	PUT_FIFO(T687_o1, 3);

	GET_FIFO(T688_i0, 0);
	GET_FIFO(T688_i1, 2);
	Butterfly(T688_i0, T688_i1, &T688_o0, &T688_o1, T688_W);
	PUT_FIFO(T688_o0, 0);
	PUT_FIFO(T688_o1, 1);

	GET_FIFO(T689_i0, 0);
	GET_FIFO(T689_i1, 2);
	Butterfly(T689_i0, T689_i1, &T689_o0, &T689_o1, T689_W);
	PUT_FIFO(T689_o0, 0);
	PUT_FIFO(T689_o1, 1);

	GET_FIFO(T690_i0, 1);
	GET_FIFO(T690_i1, 3);
	Butterfly(T690_i0, T690_i1, &T690_o0, &T690_o1, T690_W);
	PUT_FIFO(T690_o0, 0);
	PUT_FIFO(T690_o1, 1);

	GET_FIFO(T691_i0, 1);
	GET_FIFO(T691_i1, 3);
	Butterfly(T691_i0, T691_i1, &T691_o0, &T691_o1, T691_W);
	PUT_FIFO(T691_o0, 0);
	PUT_FIFO(T691_o1, 1);

	GET_FIFO(T692_i0, 0);
	GET_FIFO(T692_i1, 2);
	Butterfly(T692_i0, T692_i1, &T692_o0, &T692_o1, T692_W);
	PUT_FIFO(T692_o0, 2);
	PUT_FIFO(T692_o1, 3);

	GET_FIFO(T693_i0, 0);
	GET_FIFO(T693_i1, 2);
	Butterfly(T693_i0, T693_i1, &T693_o0, &T693_o1, T693_W);
	PUT_FIFO(T693_o0, 2);
	PUT_FIFO(T693_o1, 3);

	GET_FIFO(T694_i0, 1);
	GET_FIFO(T694_i1, 3);
	Butterfly(T694_i0, T694_i1, &T694_o0, &T694_o1, T694_W);
	PUT_FIFO(T694_o0, 2);
	PUT_FIFO(T694_o1, 3);

	GET_FIFO(T695_i0, 1);
	GET_FIFO(T695_i1, 3);
	Butterfly(T695_i0, T695_i1, &T695_o0, &T695_o1, T695_W);
	PUT_FIFO(T695_o0, 2);
	PUT_FIFO(T695_o1, 3);

	GET_FIFO(T696_i0, 0);
	GET_FIFO(T696_i1, 2);
	Butterfly(T696_i0, T696_i1, &T696_o0, &T696_o1, T696_W);
	PUT_FIFO(T696_o0, 0);
	PUT_FIFO(T696_o1, 1);

	GET_FIFO(T697_i0, 0);
	GET_FIFO(T697_i1, 2);
	Butterfly(T697_i0, T697_i1, &T697_o0, &T697_o1, T697_W);
	PUT_FIFO(T697_o0, 0);
	PUT_FIFO(T697_o1, 1);

	GET_FIFO(T698_i0, 1);
	GET_FIFO(T698_i1, 3);
	Butterfly(T698_i0, T698_i1, &T698_o0, &T698_o1, T698_W);
	PUT_FIFO(T698_o0, 0);
	PUT_FIFO(T698_o1, 1);

	GET_FIFO(T699_i0, 1);
	GET_FIFO(T699_i1, 3);
	Butterfly(T699_i0, T699_i1, &T699_o0, &T699_o1, T699_W);
	PUT_FIFO(T699_o0, 0);
	PUT_FIFO(T699_o1, 1);

	GET_FIFO(T700_i0, 0);
	GET_FIFO(T700_i1, 2);
	Butterfly(T700_i0, T700_i1, &T700_o0, &T700_o1, T700_W);
	PUT_FIFO(T700_o0, 2);
	PUT_FIFO(T700_o1, 3);

	GET_FIFO(T701_i0, 0);
	GET_FIFO(T701_i1, 2);
	Butterfly(T701_i0, T701_i1, &T701_o0, &T701_o1, T701_W);
	PUT_FIFO(T701_o0, 2);
	PUT_FIFO(T701_o1, 3);

	GET_FIFO(T702_i0, 1);
	GET_FIFO(T702_i1, 3);
	Butterfly(T702_i0, T702_i1, &T702_o0, &T702_o1, T702_W);
	PUT_FIFO(T702_o0, 2);
	PUT_FIFO(T702_o1, 3);

	GET_FIFO(T703_i0, 1);
	GET_FIFO(T703_i1, 3);
	Butterfly(T703_i0, T703_i1, &T703_o0, &T703_o1, T703_W);
	PUT_FIFO(T703_o0, 2);
	PUT_FIFO(T703_o1, 3);

	GET_FIFO(T704_i0, 0);
	GET_FIFO(T704_i1, 2);
	Butterfly(T704_i0, T704_i1, &T704_o0, &T704_o1, T704_W);
	PUT_FIFO(T704_o0, 0);
	PUT_FIFO(T704_o1, 1);

	GET_FIFO(T705_i0, 0);
	GET_FIFO(T705_i1, 2);
	Butterfly(T705_i0, T705_i1, &T705_o0, &T705_o1, T705_W);
	PUT_FIFO(T705_o0, 0);
	PUT_FIFO(T705_o1, 1);

	GET_FIFO(T706_i0, 1);
	GET_FIFO(T706_i1, 3);
	Butterfly(T706_i0, T706_i1, &T706_o0, &T706_o1, T706_W);
	PUT_FIFO(T706_o0, 0);
	PUT_FIFO(T706_o1, 1);

	GET_FIFO(T707_i0, 1);
	GET_FIFO(T707_i1, 3);
	Butterfly(T707_i0, T707_i1, &T707_o0, &T707_o1, T707_W);
	PUT_FIFO(T707_o0, 0);
	PUT_FIFO(T707_o1, 1);

	GET_FIFO(T708_i0, 0);
	GET_FIFO(T708_i1, 2);
	Butterfly(T708_i0, T708_i1, &T708_o0, &T708_o1, T708_W);
	PUT_FIFO(T708_o0, 2);
	PUT_FIFO(T708_o1, 3);

	GET_FIFO(T709_i0, 0);
	GET_FIFO(T709_i1, 2);
	Butterfly(T709_i0, T709_i1, &T709_o0, &T709_o1, T709_W);
	PUT_FIFO(T709_o0, 2);
	PUT_FIFO(T709_o1, 3);

	GET_FIFO(T710_i0, 1);
	GET_FIFO(T710_i1, 3);
	Butterfly(T710_i0, T710_i1, &T710_o0, &T710_o1, T710_W);
	PUT_FIFO(T710_o0, 2);
	PUT_FIFO(T710_o1, 3);

	GET_FIFO(T711_i0, 1);
	GET_FIFO(T711_i1, 3);
	Butterfly(T711_i0, T711_i1, &T711_o0, &T711_o1, T711_W);
	PUT_FIFO(T711_o0, 2);
	PUT_FIFO(T711_o1, 3);

	GET_FIFO(T712_i0, 0);
	GET_FIFO(T712_i1, 2);
	Butterfly(T712_i0, T712_i1, &T712_o0, &T712_o1, T712_W);
	PUT_FIFO(T712_o0, 0);
	PUT_FIFO(T712_o1, 1);

	GET_FIFO(T713_i0, 0);
	GET_FIFO(T713_i1, 2);
	Butterfly(T713_i0, T713_i1, &T713_o0, &T713_o1, T713_W);
	PUT_FIFO(T713_o0, 0);
	PUT_FIFO(T713_o1, 1);

	GET_FIFO(T714_i0, 1);
	GET_FIFO(T714_i1, 3);
	Butterfly(T714_i0, T714_i1, &T714_o0, &T714_o1, T714_W);
	PUT_FIFO(T714_o0, 0);
	PUT_FIFO(T714_o1, 1);

	GET_FIFO(T715_i0, 1);
	GET_FIFO(T715_i1, 3);
	Butterfly(T715_i0, T715_i1, &T715_o0, &T715_o1, T715_W);
	PUT_FIFO(T715_o0, 0);
	PUT_FIFO(T715_o1, 1);

	GET_FIFO(T716_i0, 0);
	GET_FIFO(T716_i1, 2);
	Butterfly(T716_i0, T716_i1, &T716_o0, &T716_o1, T716_W);
	PUT_FIFO(T716_o0, 2);
	PUT_FIFO(T716_o1, 3);

	GET_FIFO(T717_i0, 0);
	GET_FIFO(T717_i1, 2);
	Butterfly(T717_i0, T717_i1, &T717_o0, &T717_o1, T717_W);
	PUT_FIFO(T717_o0, 2);
	PUT_FIFO(T717_o1, 3);

	GET_FIFO(T718_i0, 1);
	GET_FIFO(T718_i1, 3);
	Butterfly(T718_i0, T718_i1, &T718_o0, &T718_o1, T718_W);
	PUT_FIFO(T718_o0, 2);
	PUT_FIFO(T718_o1, 3);

	GET_FIFO(T719_i0, 1);
	GET_FIFO(T719_i1, 3);
	Butterfly(T719_i0, T719_i1, &T719_o0, &T719_o1, T719_W);
	PUT_FIFO(T719_o0, 2);
	PUT_FIFO(T719_o1, 3);

	GET_FIFO(T720_i0, 0);
	GET_FIFO(T720_i1, 2);
	Butterfly(T720_i0, T720_i1, &T720_o0, &T720_o1, T720_W);
	PUT_FIFO(T720_o0, 0);
	PUT_FIFO(T720_o1, 1);

	GET_FIFO(T721_i0, 0);
	GET_FIFO(T721_i1, 2);
	Butterfly(T721_i0, T721_i1, &T721_o0, &T721_o1, T721_W);
	PUT_FIFO(T721_o0, 0);
	PUT_FIFO(T721_o1, 1);

	GET_FIFO(T722_i0, 1);
	GET_FIFO(T722_i1, 3);
	Butterfly(T722_i0, T722_i1, &T722_o0, &T722_o1, T722_W);
	PUT_FIFO(T722_o0, 0);
	PUT_FIFO(T722_o1, 1);

	GET_FIFO(T723_i0, 1);
	GET_FIFO(T723_i1, 3);
	Butterfly(T723_i0, T723_i1, &T723_o0, &T723_o1, T723_W);
	PUT_FIFO(T723_o0, 0);
	PUT_FIFO(T723_o1, 1);

	GET_FIFO(T724_i0, 0);
	GET_FIFO(T724_i1, 2);
	Butterfly(T724_i0, T724_i1, &T724_o0, &T724_o1, T724_W);
	PUT_FIFO(T724_o0, 2);
	PUT_FIFO(T724_o1, 3);

	GET_FIFO(T725_i0, 0);
	GET_FIFO(T725_i1, 2);
	Butterfly(T725_i0, T725_i1, &T725_o0, &T725_o1, T725_W);
	PUT_FIFO(T725_o0, 2);
	PUT_FIFO(T725_o1, 3);

	GET_FIFO(T726_i0, 1);
	GET_FIFO(T726_i1, 3);
	Butterfly(T726_i0, T726_i1, &T726_o0, &T726_o1, T726_W);
	PUT_FIFO(T726_o0, 2);
	PUT_FIFO(T726_o1, 3);

	GET_FIFO(T727_i0, 1);
	GET_FIFO(T727_i1, 3);
	Butterfly(T727_i0, T727_i1, &T727_o0, &T727_o1, T727_W);
	PUT_FIFO(T727_o0, 2);
	PUT_FIFO(T727_o1, 3);

	GET_FIFO(T728_i0, 0);
	GET_FIFO(T728_i1, 2);
	Butterfly(T728_i0, T728_i1, &T728_o0, &T728_o1, T728_W);
	PUT_FIFO(T728_o0, 0);
	PUT_FIFO(T728_o1, 1);

	GET_FIFO(T729_i0, 0);
	GET_FIFO(T729_i1, 2);
	Butterfly(T729_i0, T729_i1, &T729_o0, &T729_o1, T729_W);
	PUT_FIFO(T729_o0, 0);
	PUT_FIFO(T729_o1, 1);

	GET_FIFO(T730_i0, 1);
	GET_FIFO(T730_i1, 3);
	Butterfly(T730_i0, T730_i1, &T730_o0, &T730_o1, T730_W);
	PUT_FIFO(T730_o0, 0);
	PUT_FIFO(T730_o1, 1);

	GET_FIFO(T731_i0, 1);
	GET_FIFO(T731_i1, 3);
	Butterfly(T731_i0, T731_i1, &T731_o0, &T731_o1, T731_W);
	PUT_FIFO(T731_o0, 0);
	PUT_FIFO(T731_o1, 1);

	GET_FIFO(T732_i0, 0);
	GET_FIFO(T732_i1, 2);
	Butterfly(T732_i0, T732_i1, &T732_o0, &T732_o1, T732_W);
	PUT_FIFO(T732_o0, 2);
	PUT_FIFO(T732_o1, 3);

	GET_FIFO(T733_i0, 0);
	GET_FIFO(T733_i1, 2);
	Butterfly(T733_i0, T733_i1, &T733_o0, &T733_o1, T733_W);
	PUT_FIFO(T733_o0, 2);
	PUT_FIFO(T733_o1, 3);

	GET_FIFO(T734_i0, 1);
	GET_FIFO(T734_i1, 3);
	Butterfly(T734_i0, T734_i1, &T734_o0, &T734_o1, T734_W);
	PUT_FIFO(T734_o0, 2);
	PUT_FIFO(T734_o1, 3);

	GET_FIFO(T735_i0, 1);
	GET_FIFO(T735_i1, 3);
	Butterfly(T735_i0, T735_i1, &T735_o0, &T735_o1, T735_W);
	PUT_FIFO(T735_o0, 2);
	PUT_FIFO(T735_o1, 3);

	GET_FIFO(T736_i0, 0);
	GET_FIFO(T736_i1, 2);
	Butterfly(T736_i0, T736_i1, &T736_o0, &T736_o1, T736_W);
	PUT_FIFO(T736_o0, 0);
	PUT_FIFO(T736_o1, 1);

	GET_FIFO(T737_i0, 0);
	GET_FIFO(T737_i1, 2);
	Butterfly(T737_i0, T737_i1, &T737_o0, &T737_o1, T737_W);
	PUT_FIFO(T737_o0, 0);
	PUT_FIFO(T737_o1, 1);

	GET_FIFO(T738_i0, 1);
	GET_FIFO(T738_i1, 3);
	Butterfly(T738_i0, T738_i1, &T738_o0, &T738_o1, T738_W);
	PUT_FIFO(T738_o0, 0);
	PUT_FIFO(T738_o1, 1);

	GET_FIFO(T739_i0, 1);
	GET_FIFO(T739_i1, 3);
	Butterfly(T739_i0, T739_i1, &T739_o0, &T739_o1, T739_W);
	PUT_FIFO(T739_o0, 0);
	PUT_FIFO(T739_o1, 1);

	GET_FIFO(T740_i0, 0);
	GET_FIFO(T740_i1, 2);
	Butterfly(T740_i0, T740_i1, &T740_o0, &T740_o1, T740_W);
	PUT_FIFO(T740_o0, 2);
	PUT_FIFO(T740_o1, 3);

	GET_FIFO(T741_i0, 0);
	GET_FIFO(T741_i1, 2);
	Butterfly(T741_i0, T741_i1, &T741_o0, &T741_o1, T741_W);
	PUT_FIFO(T741_o0, 2);
	PUT_FIFO(T741_o1, 3);

	GET_FIFO(T742_i0, 1);
	GET_FIFO(T742_i1, 3);
	Butterfly(T742_i0, T742_i1, &T742_o0, &T742_o1, T742_W);
	PUT_FIFO(T742_o0, 2);
	PUT_FIFO(T742_o1, 3);

	GET_FIFO(T743_i0, 1);
	GET_FIFO(T743_i1, 3);
	Butterfly(T743_i0, T743_i1, &T743_o0, &T743_o1, T743_W);
	PUT_FIFO(T743_o0, 2);
	PUT_FIFO(T743_o1, 3);

	GET_FIFO(T744_i0, 0);
	GET_FIFO(T744_i1, 2);
	Butterfly(T744_i0, T744_i1, &T744_o0, &T744_o1, T744_W);
	PUT_FIFO(T744_o0, 0);
	PUT_FIFO(T744_o1, 1);

	GET_FIFO(T745_i0, 0);
	GET_FIFO(T745_i1, 2);
	Butterfly(T745_i0, T745_i1, &T745_o0, &T745_o1, T745_W);
	PUT_FIFO(T745_o0, 0);
	PUT_FIFO(T745_o1, 1);

	GET_FIFO(T746_i0, 1);
	GET_FIFO(T746_i1, 3);
	Butterfly(T746_i0, T746_i1, &T746_o0, &T746_o1, T746_W);
	PUT_FIFO(T746_o0, 0);
	PUT_FIFO(T746_o1, 1);

	GET_FIFO(T747_i0, 1);
	GET_FIFO(T747_i1, 3);
	Butterfly(T747_i0, T747_i1, &T747_o0, &T747_o1, T747_W);
	PUT_FIFO(T747_o0, 0);
	PUT_FIFO(T747_o1, 1);

	GET_FIFO(T748_i0, 0);
	GET_FIFO(T748_i1, 2);
	Butterfly(T748_i0, T748_i1, &T748_o0, &T748_o1, T748_W);
	PUT_FIFO(T748_o0, 2);
	PUT_FIFO(T748_o1, 3);

	GET_FIFO(T749_i0, 0);
	GET_FIFO(T749_i1, 2);
	Butterfly(T749_i0, T749_i1, &T749_o0, &T749_o1, T749_W);
	PUT_FIFO(T749_o0, 2);
	PUT_FIFO(T749_o1, 3);

	GET_FIFO(T750_i0, 1);
	GET_FIFO(T750_i1, 3);
	Butterfly(T750_i0, T750_i1, &T750_o0, &T750_o1, T750_W);
	PUT_FIFO(T750_o0, 2);
	PUT_FIFO(T750_o1, 3);

	GET_FIFO(T751_i0, 1);
	GET_FIFO(T751_i1, 3);
	Butterfly(T751_i0, T751_i1, &T751_o0, &T751_o1, T751_W);
	PUT_FIFO(T751_o0, 2);
	PUT_FIFO(T751_o1, 3);

	GET_FIFO(T752_i0, 0);
	GET_FIFO(T752_i1, 2);
	Butterfly(T752_i0, T752_i1, &T752_o0, &T752_o1, T752_W);
	PUT_FIFO(T752_o0, 0);
	PUT_FIFO(T752_o1, 1);

	GET_FIFO(T753_i0, 0);
	GET_FIFO(T753_i1, 2);
	Butterfly(T753_i0, T753_i1, &T753_o0, &T753_o1, T753_W);
	PUT_FIFO(T753_o0, 0);
	PUT_FIFO(T753_o1, 1);

	GET_FIFO(T754_i0, 1);
	GET_FIFO(T754_i1, 3);
	Butterfly(T754_i0, T754_i1, &T754_o0, &T754_o1, T754_W);
	PUT_FIFO(T754_o0, 0);
	PUT_FIFO(T754_o1, 1);

	GET_FIFO(T755_i0, 1);
	GET_FIFO(T755_i1, 3);
	Butterfly(T755_i0, T755_i1, &T755_o0, &T755_o1, T755_W);
	PUT_FIFO(T755_o0, 0);
	PUT_FIFO(T755_o1, 1);

	GET_FIFO(T756_i0, 0);
	GET_FIFO(T756_i1, 2);
	Butterfly(T756_i0, T756_i1, &T756_o0, &T756_o1, T756_W);
	PUT_FIFO(T756_o0, 2);
	PUT_FIFO(T756_o1, 3);

	GET_FIFO(T757_i0, 0);
	GET_FIFO(T757_i1, 2);
	Butterfly(T757_i0, T757_i1, &T757_o0, &T757_o1, T757_W);
	PUT_FIFO(T757_o0, 2);
	PUT_FIFO(T757_o1, 3);

	GET_FIFO(T758_i0, 1);
	GET_FIFO(T758_i1, 3);
	Butterfly(T758_i0, T758_i1, &T758_o0, &T758_o1, T758_W);
	PUT_FIFO(T758_o0, 2);
	PUT_FIFO(T758_o1, 3);

	GET_FIFO(T759_i0, 1);
	GET_FIFO(T759_i1, 3);
	Butterfly(T759_i0, T759_i1, &T759_o0, &T759_o1, T759_W);
	PUT_FIFO(T759_o0, 2);
	PUT_FIFO(T759_o1, 3);

	GET_FIFO(T760_i0, 0);
	GET_FIFO(T760_i1, 2);
	Butterfly(T760_i0, T760_i1, &T760_o0, &T760_o1, T760_W);
	PUT_FIFO(T760_o0, 0);
	PUT_FIFO(T760_o1, 1);

	GET_FIFO(T761_i0, 0);
	GET_FIFO(T761_i1, 2);
	Butterfly(T761_i0, T761_i1, &T761_o0, &T761_o1, T761_W);
	PUT_FIFO(T761_o0, 0);
	PUT_FIFO(T761_o1, 1);

	GET_FIFO(T762_i0, 1);
	GET_FIFO(T762_i1, 3);
	Butterfly(T762_i0, T762_i1, &T762_o0, &T762_o1, T762_W);
	PUT_FIFO(T762_o0, 0);
	PUT_FIFO(T762_o1, 1);

	GET_FIFO(T763_i0, 1);
	GET_FIFO(T763_i1, 3);
	Butterfly(T763_i0, T763_i1, &T763_o0, &T763_o1, T763_W);
	PUT_FIFO(T763_o0, 0);
	PUT_FIFO(T763_o1, 1);

	GET_FIFO(T764_i0, 0);
	GET_FIFO(T764_i1, 2);
	Butterfly(T764_i0, T764_i1, &T764_o0, &T764_o1, T764_W);
	PUT_FIFO(T764_o0, 2);
	PUT_FIFO(T764_o1, 3);

	GET_FIFO(T765_i0, 0);
	GET_FIFO(T765_i1, 2);
	Butterfly(T765_i0, T765_i1, &T765_o0, &T765_o1, T765_W);
	PUT_FIFO(T765_o0, 2);
	PUT_FIFO(T765_o1, 3);

	GET_FIFO(T766_i0, 1);
	GET_FIFO(T766_i1, 3);
	Butterfly(T766_i0, T766_i1, &T766_o0, &T766_o1, T766_W);
	PUT_FIFO(T766_o0, 2);
	PUT_FIFO(T766_o1, 3);

	GET_FIFO(T767_i0, 1);
	GET_FIFO(T767_i1, 3);
	Butterfly(T767_i0, T767_i1, &T767_o0, &T767_o1, T767_W);
	PUT_FIFO(T767_o0, 2);
	PUT_FIFO(T767_o1, 3);
}
