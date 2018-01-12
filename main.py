from PyQt4 import QtGui, QtCore
import sys
from cherry import Ui_mainform
from LineEdit import LineEdit
import numpy as np
import pandas as pd
import globalvar
from itertools import chain
import string

class cherryView(QtGui.QMainWindow, Ui_mainform):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        control_list = ['Positive', 'Negative']
        gene_list = ['ARK5_5', 'ARK5_6', 'ARK5_7', 'ZAK_6']
        self.addcomb(1, 2, control_list)  # index starts from 0!
        self.addLineEdit(1, 3, gene_list)
        # hiden the table view
        # self.tableView.hide()
        self.tabWidget.hide()
        self.model = QtGui.QStandardItemModel(self)
        self.tableview.setModel(self.model)
		
		# save the data from sourcePlate
        #sp1 = []
        #self.model.setHeaderData(ID, Qt.Horizontal, QVariant("ID"))
        #self.model.select()

        #signal with slot
        self.Plate.cellChanged.connect(self.cell_changed)
        self.upload.clicked.connect(self.loadFile)
        self.sourcePlate.clicked.connect(self.loadSourcePlate)
        self.sourcePlate_2.clicked.connect(self.loadSourcePlate2)
        self.picking.clicked.connect(self.cherrypicking)

    def loadSourcePlate(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        inputFile = open(fileName)
        #inputData = inputFile.readlines()
        inputData = inputFile.read().splitlines()
        inputFile.close()
        inputHeader = inputData[0]
        Header = [ header for header in inputHeader.split('\t') ]
        #print(len(Header))
        #for head in inputHeader
        inputData = inputData[1:]
        sp1 = []
        #sp1 = pd.DataFrame(inputData)
        for item in inputData:
			row = [ string for string in item.split('\t') ]
			#print(row)
			sp1.append(row)
        sp1 = pd.DataFrame(sp1, columns=Header)
        sp1['Well'] = sp1.Row+sp1.Col
        #print(sp1.head())
        globalvar.sp1 = sp1
		
    def loadSourcePlate2(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        inputFile = open(fileName)
        #inputData = inputFile.readlines()
        inputData = inputFile.read().splitlines()
        inputFile.close()
        inputHeader = inputData[0]
        Header = [ header for header in inputHeader.split('\t') ]
        #print(len(Header))
        #for head in inputHeader
        inputData = inputData[1:]
        sp1 = []
        #sp1 = pd.DataFrame(inputData)
        for item in inputData:
            row = [ string for string in item.split('\t') ]
            sp1.append(row)
        sp1 = pd.DataFrame(sp1, columns=Header)
        #sp1['Well'] = sp1.Row+sp1.Col
        #print(sp1.head())
        globalvar.sp2 = sp1


    # to use auto complete, change table cell to line edit
    def addLineEdit(self, row, col, items):
        edit = QtGui.QLineEdit()
        lineEdit = LineEdit(edit)
        model = QtGui.QStandardItemModel()
        for i, word in enumerate(items):
            item = QtGui.QStandardItem(word)
            model.setItem(i, 0, item)
        lineEdit.setModel(model)
        lineEdit.setModelColumn(0)
        self.Plate.setCellWidget(row, col, lineEdit)

    # add combox for specific cell in the table
    def addcomb(self, row, col, items):
        comb = QtGui.QComboBox()
        comb.addItems(items)
        self.Plate.setCellWidget(row, col, comb)


    def loadFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        inputFile = open(fileName)
        inputData = inputFile.read().splitlines()
        inputFile.close()
        self.tabWidget.show()
        inputHeader = inputData[0]
        Header = [ header for header in inputHeader.split('\t') ]
        #for head in inputHeader
        sp = []
        inputData = inputData[1:]
        for item in inputData:
            rowItem = [
                QtGui.QStandardItem(string)
                for string in item.split()
            ]
            #print(rowItem)
            # for string in item.split():
            #cell = QtGui.QStandardItem(string)
            self.model.appendRow(rowItem)
        for item in inputData:
			row = [ string for string in item.split('\t') ]
			#print(row)
			sp.append(row)
        sp = pd.DataFrame(sp, columns=Header)

        # self.model.setHeaderData(inputHeader)
        header = inputHeader.split()
        for i, j in enumerate(header):
			#print j
			self.model.setHeaderData(i, QtCore.Qt.Horizontal, QtCore.QVariant(j))

        self.platetab2.horizontalHeader().setVisible(True)
        self.Plate.hide()
        globalvar.pairlist = sp
        #print(globalvar.pairlist)


    def cell_changed(self):
        cur_col = self.Plate.currentColumn()
        cur_row = self.Plate.currentRow()
        cur_text = self.Plate.currentItem().text()
        tableItem = QtGui.QLineEdit()
        tableItem.setText(str(cur_text))
        self.Plate.setCellWidget(1, 7, tableItem)
	# the main part of cherry picking
    def cherrypicking(self):
		# get the unique sRNA name
		rna1 = set(globalvar.pairlist['rna1'])
		rna2 = set(globalvar.pairlist['rna2'])
		rna1 = set(chain(rna1, rna2))
		rnatypes = np.zeros(shape=(len(rna1),5))
		rnatypes = pd.DataFrame(rnatypes)
		sourcewell = rnatypes
		sourcewell = pd.DataFrame(sourcewell)
		for i, item in enumerate(rna1):
			#print(type(item))
			gene_symbol = list(globalvar.sp1.iloc[:,6])
			gene_symbol2 = list(globalvar.sp2.iloc[:,6])
			if(item in gene_symbol):
				# get the index for gene_symbol==item
				idx = [j for j, x in enumerate(gene_symbol) if x==item]
				rnatypes.iloc[i, 1:4] = list(globalvar.sp1.iloc[idx, 11])
				# save the plate ID
				rnatypes.iloc[i, 4] = globalvar.sp1.iloc[1, 0]
				sourcewell.iloc[i, 4] = globalvar.sp1.iloc[1, 0]
				sourcewell.iloc[i, 1:4] = list(globalvar.sp1.iloc[idx, 12])
			elif(item in gene_symbol2):
				idx = [j for j, x in enumerate(gene_symbol2) if x==item]
				#print(idx)
				rnatypes.iloc[i, 1:4] = list(globalvar.sp2.iloc[idx, 11])
				# save the plate ID
				rnatypes.iloc[i, 4] = globalvar.sp2.iloc[1, 0]
				sourcewell.iloc[i, 4] = globalvar.sp2.iloc[1, 0]
				sourcewell.iloc[i, 1:4] = list(globalvar.sp2.iloc[idx, 12])
		rnatypes.iloc[:, 0] = list(rna1)
		sourcewell.iloc[:, 0] = list(rna1)
		rnatypes.columns = ['name', 'siRNA1', 'siRNA2', 'siRNA3', 'sourceplate']
		sourcewell.columns = ['name', 'w1', 'w2', 'w3', 'sourceplate']
		#print(sourcewell)
		cell_line = globalvar.pairlist['cell.line']
		cline_num = set(cell_line)
		# designed plate info
		row_dp = map(chr, range(65, 91))[2:14]
		col_dp = range(3,23)

		# the echo file
		echo = []
		# transfer volumn info
		vol = [[80]*4]*4 
		vol = pd.DataFrame(vol)
		vol.iloc[0,:] = 160
		vol.iloc[:,0] = 160
		for cline in cline_num:
			subset_cl = globalvar.pairlist[globalvar.pairlist['cell.line']== cline]
	# get the plate info
			plate_sub = subset_cl['plate']
			plate = set(plate_sub)
	#print(plate)
			for each_plate in plate:
		#idx = [j for j, x in enumerate(plate_sub) if x==each_plate]
		#subset_plate = subset_cl.iloc[idx, : ]
				subset_plate = subset_cl[subset_cl['plate']==each_plate]
				for row in subset_plate.index:
					rna1 = subset_plate.at[row, 'rna1']
			# index for the sourcewell and rnatypes
			#idx_sourcewell1 = [ii for ii, xx in enumerate(sourcewell['name']) if xx== rna1]
					sourcewell1 = sourcewell[sourcewell['name']==rna1]
					rnatype1 = rnatypes[rnatypes['name']==rna1]
					rna2 = subset_plate.at[row, 'rna2']
					sourcewell2 = sourcewell[sourcewell['name']==rna2]
					rnatype2 = rnatypes[rnatypes['name']==rna2]
			# get the index info
					index_plate = subset_plate.at[row, 'index']
					index_plate = int(index_plate)-1
			# devide the plate into three rows and five columns so in total 15 4*4 array
			# which row
					if(index_plate/5==0):
						vol.index = row_dp[0:4]
					elif(index_plate/5==1):
						vol.index = row_dp[4:8]
					else:
						vol.index = row_dp[8:13]
				
			# which column
					if(index_plate%5==0):
						vol.columns = col_dp[0:4]
					elif(index_plate%5==1):
						vol.columns = col_dp[4:8]
					elif(index_plate%5==2):
						vol.columns = col_dp[8:12]
					elif(index_plate%5==3):
						vol.columns = col_dp[12:16]
					else:
						vol.columns = col_dp[16:20]
				
			# for the first siRNA
					vol1 = vol.iloc[:,1:4]
					for row_idx in range(0,4):
						for col_idx in range(0,3):
							echo_row = []
					# rna name
							echo_row.append(rna1)
					# rna type
							echo_row.append(rnatype1.iloc[0, col_idx+1])
					# rna source well
							echo_row.append(sourcewell1.iloc[0, col_idx+1])
					# rna source plate id
							echo_row.append(sourcewell1.iloc[0, 4])
					# rna vol
							echo_row.append(vol1.iloc[row_idx, col_idx])
					# destination well
							echo_row.append(vol1.index[row_idx]+str(vol1.columns[col_idx]))
							# plate index
							echo_row.append('MDA231_'+str(each_plate)+'_siRNAcombo')
							echo.append(echo_row)
			
			# for the second siRNA
					vol2 = (vol.iloc[1:4, :]).transpose()
			
					for row_idx in range(0,4):
						for col_idx in range(0,3):
							echo_row = []
					# rna name
							echo_row.append(rna2)
					# rna type
							echo_row.append(rnatype2.iloc[0, col_idx+1])
					# rna source well
							echo_row.append(sourcewell2.iloc[0, col_idx+1])
					# rna source plate id
							echo_row.append(sourcewell2.iloc[0, 4])
					# rna vol
							echo_row.append(vol2.iloc[row_idx, col_idx])
					# destination well
							echo_row.append(str(vol2.columns[col_idx])+str(vol2.index[row_idx]))
							# plate index
							echo_row.append('MDA231_'+str(each_plate)+'_siRNAcombo')
							echo.append(echo_row)
			#vol.index = row_name
			#vol.columns = col_name
			

		echo = pd.DataFrame(echo)
		
		dest_barcode = ['MDA231_1_siRNAcombo', 'MDA231_2_siRNAcombo', 'MDA231_3_siRNAcombo']
# add controls: 22 negative ctrs and 16 positive ctrs
		Ndest_well = ["B5", "B9", "B13", "B17", "B21", "C3", "C11", "C19", "F2", "F23", "G7", "G15", "I2", "I23", "K3", "K11", "K19", "O5", "O9", "O13", "O17", "O21"]
		Pdest_well = ["B3", "B12", "B22", "C7", "C15", "G3", "G11", "G19", "K7", "K15", "M2", "M23", "O7", "O11", "O15", "O19"]
		Ncontrol = pd.DataFrame( {'RNA': ['NegCtr']*22*3, 'RNAtype': ['CTR']*22*3, 'source_well': ['F3']*22*3,'Source_Plate_Barcode': ['ctr']*22*3, 'Transfer Volume': [40]*22*3,'Destination Well': Ndest_well*3, 'Destination Plate Barcode': dest_barcode*22})
		Pcontrol = pd.DataFrame( {'RNA': ['PosCtr']*16*3, 'RNAtype': ['CTR']*16*3, 'source_well': ['C3']*16*3,'Source_Plate_Barcode': ['ctr']*16*3, 'Transfer Volume': [40]*16*3,'Destination Well': Pdest_well*3, 'Destination Plate Barcode': dest_barcode*16})
		control = pd.concat([Ncontrol, Pcontrol], ignore_index=True)
		echo.columns = ['RNA', 'RNAtype', 'source_well', 'Source_Plate_Barcode', 'Transfer Volume', 'Destination Well', 'Destination Plate Barcode']
		echo = pd.concat([echo, control], ignore_index=True)
		echo['Source_Plate_Type'] = '384PP_AQ_BP2'

#writer = pd.ExcelWriter('output.xlsx')
#echo.to_excel(writer, 'Sheet1')
		outputFile = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV(*.csv)')
		#print(outputFile)
		echo.to_csv(outputFile, sep=',', header=True, index=False)
		#print(echo)
#writer.save()
		



# def main(self):
#self.show()

app = QtGui.QApplication(sys.argv)
window = cherryView(None)
window.show()
app.exec_()

