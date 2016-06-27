#fish.py
#created: 6/26/2016
#Contributors: Nick McHale,
#-------------------------------------------------------------------------
#The fish class will keep track of the fishes position over time and
#based on the position data of the fish, a unpredictable bitstream will be 
#generated
#future complexitys for bit generation could potentially be
#velocity data or acceleration data

import binascii.a2b_uu

DATA_POINTS_REQUIRED = 500

class Fish:
    
    _avgPos=None
    _position_history = []
    _bitString = ''
    _outBytes = []

#--------------------------------------------------------------------
    def __init__():




#--------------------------------------------------------------------
 
    def updatePosition(curPos=(x=None,y=None)):
        #check that we have valid data.
        if ( curPos[x] == None || curPos[y] == None ):
            #ERROR you must pass data to this function
            #TODO should probably add some debug logging here
            return

        #Have we collected enough data about the subject?
        if  len(_position_history) < DATA_POINTS_REQUIRED:
            _position_history.append(curPos)
        
        else
            #if we have enough data, but have not yet calculated our average position
            # then do it now
            if _avgPos == None:
                _calculate_average()
            
            #ok now we can get some bits
            _makeBits(curPos)

#--------------------------------------------------------------------
    def _makeBits( pos=(x=None, y=None) ):
        
        if pos[x] < _avgPos[x]:
            _bitString = _bitString + '1'
        else
            _bitString = _bitString + '0'

        if pos[x] < _avgPos[x]:
            _bitString = _bitString + '1'
        else
            _bitString = _bitString + '0'

        
        if len(_bitString >= 8):
            next_byte = _bitString[:8]
            _bitString = _bitString[8:]#TODO THIS MIGHT CAUSE INDEX OUT OF BOUNS.... CHECK IT
            _outBytes.append(binascii.a2b_uu(next_byte))


#--------------------------------------------------------------------
 
    def _calculate_average():
        
        num_data_points = len(_position_history)
        cumulativeX = 0.0
        cumulativeY = 0.0
        
        for pos in _position_history:
            cumulativeX += float(pos[x])
            cumulativeY += float(pos[y])

        averageX = cumulativeX / num_data_points
        averageY = cumulativeY / num_data_points

        _avgPos = (avgX = averageX, avgY = averageY)

#--------------------------------------------------------------------
#getBytes will return to the caller an array of bytes that have been 
#generated in a unpredictable fashon.
#if this function is called before enough data has been generated,
#then an empty array will be returned

    def getBytes():
        
        out_bytes = _outBytes
        _outBytes = []
        return out_bytes

#--------------------------------------------------------------------
 
#--------------------------------------------------------------------
 
#--------------------------------------------------------------------
 
