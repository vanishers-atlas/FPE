library ieee;
use ieee.std_logic_1164.all;
library work;
use work.ssp_pkg.all;

entity spu_brdetc is
	generic (
	PC_ADDR_WIDTH : integer :=  6;
	BRANCH_EN	: boolean	:= true;
	JMP_EN		: boolean	:= true
	);
	port (
		i_id_beq		:   in std_logic;
		i_id_bgt		:   in std_logic;
		i_id_blt		:   in std_logic;
		i_id_bge		:   in std_logic;
		i_id_ble		:   in std_logic;
		i_id_bne		:   in std_logic;

		i_ex_zero		:   in std_logic;
		i_ex_sign	:   in std_logic;
		o_branch_taken	:   out std_logic;
		
		i_id_b			:	in std_logic;
		o_jmp_taken	:   out std_logic
	);
end spu_brdetc;

architecture structure of spu_brdetc is
  signal branch_taken: std_logic := '0';
  signal jmp_taken : std_logic := '0';
begin
  o_jmp_taken <= 	jmp_taken;
  o_branch_taken <= branch_taken;
  
	branch_sig_gen: if BRANCH_EN = true generate
		branch_taken <= (i_id_beq and i_ex_zero) or (i_id_bgt and (not i_ex_sign) and (not i_ex_zero)) or 
                    (i_id_blt and i_ex_sign) or (i_id_bge or (not i_ex_sign)) or 
                    (i_id_ble and (i_ex_zero or i_ex_sign)) or (i_id_bne and (not i_ex_zero));
	end generate;
	
	jmp_sig_gen: if JMP_EN = true generate
		jmp_taken <= i_id_b;
	end generate;

end structure;
