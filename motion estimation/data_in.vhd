library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
use ieee.std_logic_textio.all;
use std.textio.all;
library unisim;
use unisim.vcomponents.all;
library work;
use work.ssp_pkg.all;
use work.ssp_typedef.all;

entity data_in is
  generic(
    ARRAY_NUM    : integer := 128;
    RF_IO_WIDTH  : integer := 16
  );
  port (     
    clk         : in    std_logic;
    o_rst       : out   std_logic;
    i_pm_finish : in    std_logic;
    
    o_data      : out   VDATA_TYPE(ARRAY_NUM-1 downto 0);
    o_data_wen  : out   VSIG_TYPE(ARRAY_NUM-1 downto 0)
  );    
end data_in;

architecture structure of data_in is

procedure data_in_procedure
  ( FILE infile : TEXT;
    signal data_P: out std_logic_vector(RF_IO_WIDTH-1 downto 0);
    signal data_wen_P: out std_logic;
    constant num : integer )
is 
  variable ramfileline : LINE;
  variable data_line : std_logic_vector(RF_IO_WIDTH-1 downto 0);
  variable signo  : integer;
  variable i : integer := 0;
begin

  while i < num loop
    wait until clk'event and clk = '0';
    if ENDFILE(infile) then
      data_P <= (others => 'Z');
      data_wen_P <= '0';
      exit;
    else
      readline (infile, ramfileline);        
      
      if ramfileline(ramfileline'left) = '/' then
        next;
      end if;
      
      signo := RF_IO_WIDTH-1;
      for m in ramfileline'range loop
        case ramfileline(m) is
          when '0' => data_line(signo) := '0';
          when '1' => data_line(signo) := '1';
          when ' ' | HT => next;
          when '/' => exit;
          when others => next;
        end case;
        
        signo := signo -1;                
      end loop;
      
      data_P <= data_line;
      data_wen_P <= '1';    
      i := i + 1;
    end if;
  end loop;

end procedure data_in_procedure;

signal data : VDATA_TYPE(ARRAY_NUM-1 downto 0);
signal data_wen : VSIG_TYPE(ARRAY_NUM-1 downto 0) := (others=>'0');
signal rst : std_logic := '1';

FILE data_in_file_0 : TEXT open READ_MODE is "DataIn/data_in_0.dat";
FILE data_in_file_1 : TEXT open READ_MODE is "DataIn/data_in_1.dat";
FILE data_in_file_2 : TEXT open READ_MODE is "DataIn/data_in_2.dat";
FILE data_in_file_3 : TEXT open READ_MODE is "DataIn/data_in_3.dat";
FILE data_in_file_4 : TEXT open READ_MODE is "DataIn/data_in_4.dat";
FILE data_in_file_5 : TEXT open READ_MODE is "DataIn/data_in_5.dat";
FILE data_in_file_6 : TEXT open READ_MODE is "DataIn/data_in_6.dat";
FILE data_in_file_7 : TEXT open READ_MODE is "DataIn/data_in_7.dat";
FILE data_in_file_8 : TEXT open READ_MODE is "DataIn/data_in_8.dat";
FILE data_in_file_9 : TEXT open READ_MODE is "DataIn/data_in_9.dat";
FILE data_in_file_10 : TEXT open READ_MODE is "DataIn/data_in_10.dat";
FILE data_in_file_11 : TEXT open READ_MODE is "DataIn/data_in_11.dat";
FILE data_in_file_12 : TEXT open READ_MODE is "DataIn/data_in_12.dat";
FILE data_in_file_13 : TEXT open READ_MODE is "DataIn/data_in_13.dat";
FILE data_in_file_14 : TEXT open READ_MODE is "DataIn/data_in_14.dat";
FILE data_in_file_15 : TEXT open READ_MODE is "DataIn/data_in_15.dat";
FILE data_in_file_16 : TEXT open READ_MODE is "DataIn/data_in_16.dat";
FILE data_in_file_17 : TEXT open READ_MODE is "DataIn/data_in_17.dat";
FILE data_in_file_18 : TEXT open READ_MODE is "DataIn/data_in_18.dat";
FILE data_in_file_19 : TEXT open READ_MODE is "DataIn/data_in_19.dat";
FILE data_in_file_20 : TEXT open READ_MODE is "DataIn/data_in_20.dat";
FILE data_in_file_21 : TEXT open READ_MODE is "DataIn/data_in_21.dat";
FILE data_in_file_22 : TEXT open READ_MODE is "DataIn/data_in_22.dat";
FILE data_in_file_23 : TEXT open READ_MODE is "DataIn/data_in_23.dat";
FILE data_in_file_24 : TEXT open READ_MODE is "DataIn/data_in_24.dat";
FILE data_in_file_25 : TEXT open READ_MODE is "DataIn/data_in_25.dat";
FILE data_in_file_26 : TEXT open READ_MODE is "DataIn/data_in_26.dat";
FILE data_in_file_27 : TEXT open READ_MODE is "DataIn/data_in_27.dat";
FILE data_in_file_28 : TEXT open READ_MODE is "DataIn/data_in_28.dat";
FILE data_in_file_29 : TEXT open READ_MODE is "DataIn/data_in_29.dat";
FILE data_in_file_30 : TEXT open READ_MODE is "DataIn/data_in_30.dat";
FILE data_in_file_31 : TEXT open READ_MODE is "DataIn/data_in_31.dat";

begin
  o_rst <= rst; 
  o_data <= data;    
  o_data_wen <= data_wen;
  
  start_proc: process begin
    if i_pm_finish /= '1' then
      wait until i_pm_finish = '1';
    end if;
    
    rst <= '0';
    wait;
  end process;
  
  PROC_D0: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_0, data(0), data_wen(0), 1000);
  end process;

  PROC_D1: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_1, data(1), data_wen(1), 1000);
  end process;

  PROC_D2: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_2, data(2), data_wen(2), 1000);
  end process;

  PROC_D3: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_3, data(3), data_wen(3), 1000);
  end process;

  PROC_D4: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_4, data(4), data_wen(4), 1000);
  end process;

  PROC_D5: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_5, data(5), data_wen(5), 1000);
  end process;

  PROC_D6: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_6, data(6), data_wen(6), 1000);
  end process;

  PROC_D7: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_7, data(7), data_wen(7), 1000);
  end process;

  PROC_D8: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_8, data(8), data_wen(8), 1000);
  end process;

  PROC_D9: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_9, data(9), data_wen(9), 1000);
  end process;

  PROC_D10: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_10, data(10), data_wen(10), 1000);
  end process;

  PROC_D11: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_11, data(11), data_wen(11), 1000);
  end process;

  PROC_D12: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_12, data(12), data_wen(12), 1000);
  end process;

  PROC_D13: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_13, data(13), data_wen(13), 1000);
  end process;

  PROC_D14: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_14, data(14), data_wen(14), 1000);
  end process;

  PROC_D15: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_15, data(15), data_wen(15), 1000);
  end process;

  PROC_D16: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_16, data(16), data_wen(16), 1000);
  end process;

  PROC_D17: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_17, data(17), data_wen(17), 1000);
  end process;

  PROC_D18: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_18, data(18), data_wen(18), 1000);
  end process;

  PROC_D19: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_19, data(19), data_wen(19), 1000);
  end process;

  PROC_D20: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_20, data(20), data_wen(20), 1000);
  end process;

  PROC_D21: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_21, data(21), data_wen(21), 1000);
  end process;

  PROC_D22: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_22, data(22), data_wen(22), 1000);
  end process;

  PROC_D23: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_23, data(23), data_wen(23), 1000);
  end process;

  PROC_D24: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_24, data(24), data_wen(24), 1000);
  end process;

  PROC_D25: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_25, data(25), data_wen(25), 1000);
  end process;

  PROC_D26: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_26, data(26), data_wen(26), 1000);
  end process;

  PROC_D27: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_27, data(27), data_wen(27), 1000);
  end process;

  PROC_D28: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_28, data(28), data_wen(28), 1000);
  end process;

  PROC_D29: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_29, data(29), data_wen(29), 1000);
  end process;

  PROC_D30: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_30, data(30), data_wen(30), 1000);
  end process;

  PROC_D31: process begin
    wait until rst = '0';
    data_in_procedure(data_in_file_31, data(31), data_wen(31), 1000);
  end process;

end structure;