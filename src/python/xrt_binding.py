"""
 Copyright (C) 2019 Xilinx, Inc

 ctypes based Python binding for XRT

 Licensed under the Apache License, Version 2.0 (the "License"). You may
 not use this file except in compliance with the License. A copy of the
 License is located at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 License for the specific language governing permissions and limitations
 under the License.
"""

import os
import errno
import ctypes

from xclbin_binding import *
from ert_binding import *

libcore = ctypes.CDLL(os.environ['XILINX_XRT'] + "/lib/libxrt_core.so", mode=ctypes.RTLD_GLOBAL)
libcoreutil = ctypes.CDLL(os.environ['XILINX_XRT'] + "/lib/libxrt_coreutil.so", mode=ctypes.RTLD_GLOBAL)

xclDeviceHandle = ctypes.c_void_p
xrtKernelHandle = ctypes.c_void_p
xrtRunHandle = ctypes.c_void_p
xrtKernelRunHandle = ctypes.c_void_p

class xclDeviceInfo2(ctypes.Structure):
    # "_fields_" is a required keyword
    _fields_ = [
     ("mMagic", ctypes.c_uint),
     ("mName", ctypes.c_char*256),
     ("mHALMajorVersion", ctypes.c_ushort),
     ("mHALMinorVersion", ctypes.c_ushort),
     ("mVendorId", ctypes.c_ushort),
     ("mDeviceId", ctypes.c_ushort),
     ("mSubsystemId", ctypes.c_ushort),
     ("mSubsystemVendorId", ctypes.c_ushort),
     ("mDeviceVersion", ctypes.c_ushort),
     ("mDDRSize", ctypes.c_size_t),
     ("mDataAlignment", ctypes.c_size_t),
     ("mDDRFreeSize", ctypes.c_size_t),
     ("mMinTransferSize", ctypes.c_size_t),
     ("mDDRBankCount", ctypes.c_ushort),
     ("mOCLFrequency", ctypes.c_ushort*4),
     ("mPCIeLinkWidth", ctypes.c_ushort),
     ("mPCIeLinkSpeed", ctypes.c_ushort),
     ("mDMAThreads", ctypes.c_ushort),
     ("mOnChipTemp", ctypes.c_short),
     ("mFanTemp", ctypes.c_short),
     ("mVInt", ctypes.c_ushort),
     ("mVAux", ctypes.c_ushort),
     ("mVBram", ctypes.c_ushort),
     ("mCurrent", ctypes.c_float),
     ("mNumClocks", ctypes.c_ushort),
     ("mFanSpeed", ctypes.c_ushort),
     ("mMigCalib", ctypes.c_bool),
     ("mXMCVersion", ctypes.c_ulonglong),
     ("mMBVersion", ctypes.c_ulonglong),
     ("m12VPex", ctypes.c_short),
     ("m12VAux", ctypes.c_short),
     ("mPexCurr", ctypes.c_ulonglong),
     ("mAuxCurr", ctypes.c_ulonglong),
     ("mFanRpm", ctypes.c_ushort),
     ("mDimmTemp", ctypes.c_ushort*4),
     ("mSE98Temp", ctypes.c_ushort*4),
     ("m3v3Pex", ctypes.c_ushort),
     ("m3v3Aux", ctypes.c_ushort),
     ("mDDRVppBottom",ctypes.c_ushort),
     ("mDDRVppTop", ctypes.c_ushort),
     ("mSys5v5", ctypes.c_ushort),
     ("m1v2Top", ctypes.c_ushort),
     ("m1v8Top", ctypes.c_ushort),
     ("m0v85", ctypes.c_ushort),
     ("mMgt0v9", ctypes.c_ushort),
     ("m12vSW", ctypes.c_ushort),
     ("mMgtVtt", ctypes.c_ushort),
     ("m1v2Bottom", ctypes.c_ushort),
     ("mDriverVersion, ", ctypes.c_ulonglong),
     ("mPciSlot", ctypes.c_uint),
     ("mIsXPR", ctypes.c_bool),
     ("mTimeStamp", ctypes.c_ulonglong),
     ("mFpga", ctypes.c_char*256),
     ("mPCIeLinkWidthMax", ctypes.c_ushort),
     ("mPCIeLinkSpeedMax", ctypes.c_ushort),
     ("mVccIntVol", ctypes.c_ushort),
     ("mVccIntCurr", ctypes.c_ushort),
     ("mNumCDMA", ctypes.c_ushort)
    ]

# Unused, keep for backwards compatibility
class xclBOKind:
    XCL_BO_SHARED_VIRTUAL           = 0
    XCL_BO_SHARED_PHYSICAL          = 1
    XCL_BO_MIRRORED_VIRTUAL         = 2
    XCL_BO_DEVICE_RAM               = 3
    XCL_BO_DEVICE_BRAM              = 4
    XCL_BO_DEVICE_PREALLOCATED_BRAM = 5

class xclBOSyncDirection:
    XCL_BO_SYNC_BO_TO_DEVICE   = 0
    XCL_BO_SYNC_BO_FROM_DEVICE = 1

class xclAddressSpace:
    XCL_ADDR_SPACE_DEVICE_FLAT    = 0  # Absolute address space
    XCL_ADDR_SPACE_DEVICE_RAM     = 1  # Address space for the DDR memory
    XCL_ADDR_KERNEL_CTRL          = 2  # Address space for the OCL Region control port
    XCL_ADDR_SPACE_DEVICE_PERFMON = 3  # Address space for the Performance monitors
    XCL_ADDR_SPACE_DEVICE_CHECKER = 5  # Address space for protocol checker
    XCL_ADDR_SPACE_MAX = 8

# Defines log message severity levels for messages sent to log file with xclLogMsg cmd
class xrtLogMsgLevel:
    XRT_EMERGENCY = 0
    XRT_ALERT     = 1
    XRT_CRITICAL  = 2
    XRT_ERROR     = 3
    XRT_WARNING   = 4
    XRT_NOTICE    = 5
    XRT_INFO      = 6
    XRT_DEBUG     = 7

# Defines log message severity levels for messages sent to log file with xclLogMsg cmd
class xclVerbosityLevel:
    XCL_QUIET = 0
    XCL_INFO  = 1
    XCL_WARN  = 2
    XCL_ERROR = 3

class xclResetKind:
    XCL_RESET_KERNEL = 0
    XCL_RESET_FULL   = 1
    XCL_USER_RESET   = 2

class xclDeviceUsage (ctypes.Structure):
    _fields_ = [
     ("h2c", ctypes.c_size_t*8),
     ("c2h", ctypes.c_size_t*8),
     ("ddeMemUsed", ctypes.c_size_t*8),
     ("ddrBOAllocated", ctypes.c_uint *8),
     ("totalContents", ctypes.c_uint),
     ("xclbinId", ctypes.c_ulonglong),
     ("dma_channel_cnt", ctypes.c_uint),
     ("mm_channel_cnt", ctypes.c_uint),
     ("memSize", ctypes.c_ulonglong*8)
    ]

class xclBOProperties (ctypes.Structure):
    _fields_ = [
     ("handle", ctypes.c_uint),
     ("flags" , ctypes.c_uint),
     ("size", ctypes.c_ulonglong),
     ("paddr", ctypes.c_ulonglong),
     ("reserved", ctypes.c_uint), # not implemented
    ]

def _valueOrError(res):
    """
    Validate return code from XRT C library and raise an exception if necessary
    """
    if (res < 0):
        res = -res
        raise OSError(res, os.strerror(res))
    return res


def xclProbe():
    """
    xclProbe() - Enumerate devices found in the system
    :return: count of devices found
    """
    return libcore.xclProbe()

def xclVersion():
    """
    :return: the version number. 1 => Hal1 ; 2 => Hal2
    """
    return libcore.xclVersion()

def xclOpen(deviceIndex, logFileName, level):
    """
    xclOpen(): Open a device and obtain its handle

    :param deviceIndex: (unsigned int) Slot number of device 0 for first device, 1 for the second device...
    :param logFileName: (const char pointer) Log file to use for optional logging
    :param level: (int) Severity level of messages to log
    :return: device handle
    """
    libcore.xclOpen.restype = ctypes.POINTER(xclDeviceHandle)
    libcore.xclOpen.argtypes = [ctypes.c_uint, ctypes.c_char_p, ctypes.c_int]
    return _valueOrError(libcore.xclOpen(deviceIndex, logFileName, level))


def xclClose(handle):
    """
    xclClose(): Close an opened device

    :param handle: (xclDeviceHandle) device handle
    :return: None
    """
    libcore.xclClose.restype = None
    libcore.xclClose.argtype = xclDeviceHandle
    libcore.xclClose(handle)

def xclResetDevice(handle, kind):
    """
    xclResetDevice() - Reset a device or its CL
    :param handle: Device handle
    :param kind: Reset kind
    :return: 0 on success or appropriate error number
    """
    libcore.xclResetDevice.restype = ctypes.c_int
    libcore.xclResetDevice.argtypes = [xclDeviceHandle, ctypes.c_int]
    libcore.xclResetDevice(handle, kind)

def xclGetDeviceInfo2 (handle, info):
    """
    xclGetDeviceInfo2() - Obtain various bits of information from the device

    :param handle: (xclDeviceHandle) device handle
    :param info: (xclDeviceInfo pointer) Information record
    :return: 0 on success or appropriate error number
    """

    libcore.xclGetDeviceInfo2.restype = ctypes.c_int
    libcore.xclGetDeviceInfo2.argtypes = [xclDeviceHandle, ctypes.POINTER(xclDeviceInfo2)]
    return _valueOrError(libcore.xclGetDeviceInfo2(handle, info))


def xclGetUsageInfo (handle, info):
    """
    xclGetUsageInfo() - Obtain usage information from the device
    :param handle: Device handle
    :param info: Information record
    :return: 0 on success or appropriate error number
    """
    libcore.xclGetUsageInfo.restype = ctypes.c_int
    libcore.xclGetUsageInfo.argtypes = [xclDeviceHandle, ctypes.POINTER(xclDeviceInfo2)]
    return _valueOrError(libcore.xclGetUsageInfo(handle, info))


def xclGetErrorStatus(handle, info):
    """
    xclGetErrorStatus() - Obtain error information from the device
    :param handle: Device handle
    :param info: Information record
    :return: 0 on success or appropriate error number
    """
    libcore.xclGetErrorStatus.restype = ctypes.c_int
    libcore.xclGetErrorStatus.argtypes = [xclDeviceHandle, ctypes.POINTER(xclDeviceInfo2)]
    return _valueOrError(libcore.xclGetErrorStatus(handle, info))


def xclLoadXclBin(handle, buf):
    """
    Download FPGA image (xclbin) to the device

    :param handle: (xclDeviceHandle) device handle
    :param buf: (void pointer) Pointer to device image (xclbin) in memory
    :return: 0 on success or appropriate error number

    Download FPGA image (AXLF) to the device. The PR bitstream is encapsulated inside
    xclbin as a section. xclbin may also contains other sections which are suitably
    handled by the driver
    """
    libcore.xclLoadXclBin.restype = ctypes.c_int
    libcore.xclLoadXclBin.argtypes = [xclDeviceHandle, ctypes.c_void_p]
    return _valueOrError(libcore.xclLoadXclBin(handle, buf))


def xclGetSectionInfo(handle, info, size, kind, index):
    """
    xclGetSectionInfo() - Get Information from sysfs about the downloaded xclbin sections
    :param handle: Device handle
    :param info: Pointer to preallocated memory which will store the return value.
    :param size: Pointer to preallocated memory which will store the return size.
    :param kind: axlf_section_kind for which info is being queried
    :param index: The (sub)section index for the "kind" type.
    :return: 0 on success or appropriate error number
    """
    libcore.xclGetSectionInfo.restype = ctypes.c_int
    libcore.xclGetSectionInfo.argtypes = [xclDeviceHandle, ctypes.POINTER(xclDeviceInfo2),
                                       ctypes.POINTER(ctypes.sizeof(xclDeviceInfo2)),
                                       ctypes.c_int, ctypes.c_int]
    return _valueOrError(libcore.xclGetSectionInfo(handle, info, size, kind, index))


def xclReClock2(handle, region, targetFreqMHz):
    """
    xclReClock2() - Configure PR region frequencies
    :param handle: Device handle
    :param region: PR region (always 0)
    :param targetFreqMHz: Array of target frequencies in order for the Clock Wizards driving the PR region
    :return: 0 on success or appropriate error number
    """
    libcore.xclReClock2.restype = ctypes.c_int
    libcore.xclReClock2.argtypes = [xclDeviceHandle, ctypes.c_uint, ctypes.c_uint]
    return _valueOrError(libcore.xclReClock2(handle, region, targetFreqMHz))


def xclLockDevice(handle):
    """
    The function is NOP; it exists for backward compatiblity.
    """
    return 0

def xclUnlockDevice(handle):
    """
    The function is NOP; it exists for backward compatiblity.
    """
    return 0

def xclOpenContext(handle, xclbinId, ipIndex, shared):
    """
    xclOpenContext() - Create shared/exclusive context on compute units
    :param handle: Device handle
    :param xclbinId: UUID of the xclbin image running on the device
    :param ipIndex: IP/CU index in the IP LAYOUT array
    :param shared: Shared access or exclusive access
    :return: 0 on success or appropriate error number

    The context is necessary before submitting execution jobs using xclExecBuf(). Contexts may be
    exclusive or shared. Allocation of exclusive contexts on a compute unit would succeed
    only if another client has not already setup up a context on that compute unit. Shared
    contexts can be concurrently allocated by many processes on the same compute units.
    """
    libcore.xclOpenContext.restype = ctypes.c_int
    libcore.xclOpenContext.argtypes = [xclDeviceHandle, ctypes.c_char_p, ctypes.c_uint, ctypes.c_bool]
    return _valueOrError(libcore.xclOpenContext(handle, xclbinId.bytes, ipIndex, shared))


def xclCloseContext(handle, xclbinId, ipIndex):
    """
    xclCloseContext() - Close previously opened context
    :param handle: Device handle
    :param xclbinId: UUID of the xclbin image running on the device
    :param ipIndex: IP/CU index in the IP LAYOUT array
    :return: 0 on success or appropriate error number

    Close a previously allocated shared/exclusive context for a compute unit.
    """
    libcore.xclCloseContext.restype = ctypes.c_int
    libcore.xclCloseContext.argtypes = [xclDeviceHandle, ctypes.c_char_p, ctypes.c_uint]
    return _valueOrError(libcore.xclCloseContext(handle, xclbinId.bytes, ipIndex))


def xclUpgradeFirmware(handle, fileName):
    """
    Update the device BPI PROM with new image
    :param handle: Device handle
    :param fileName:
    :return: 0 on success or appropriate error number
    """
    libcore.xclUpgradeFirmware.restype = ctypes.c_int
    libcore.xclUpgradeFirmware.argtypes = [xclDeviceHandle, ctypes.c_void_p]
    return libcore.xclUpgradeFirmware(handle, fileName)

def xclUpgradeFirmware2(handle, file1, file2):
    """
    Update the device BPI PROM with new image with clearing bitstream
    :param handle: Device handle
    :param fileName:
    :return: 0 on success or appropriate error number
    """
    libcore.xclUpgradeFirmware2.restype = ctypes.c_int
    libcore.xclUpgradeFirmware2.argtypes = [xclDeviceHandle, ctypes.c_void_p, ctypes.c_void_p]
    return libcore.xclUpgradeFirmware2(handle, file1, file2)

def xclUpgradeFirmwareXSpi (handle, fileName, index):
    """
    Update the device SPI PROM with new image
    :param handle:
    :param fileName:
    :param index:
    :return:
    """
    libcore.xclUpgradeFirmwareXSpi.restype = ctypes.c_int
    libcore.xclUpgradeFirmwareXSpi.argtypes = [xclDeviceHandle, ctypes.c_void_p, ctypes.c_int]
    return libcore.xclUpgradeFirmwareXSpi(handle, fileName, index)

def xclBootFPGA(handle):
    """
    Boot the FPGA from PROM
    :param handle: Device handle
    :return: 0 on success or appropriate error number
    """
    libcore.xclBootFPGA.restype = ctypes.c_int
    libcore.xclBootFPGA.argtype = xclDeviceHandle
    return libcore.xclBootFPGA(handle)

def xclRemoveAndScanFPGA():
    """
    Write to /sys/bus/pci/devices/<deviceHandle>/remove and initiate a pci rescan by
    writing to /sys/bus/pci/rescan.
    :return:
    """
    libcore.xclRemoveAndScanFPGA.restype = ctypes.c_int
    return libcore.xclRemoveAndScanFPGA()

def xclLogMsg(handle, level, tag, format, *args):
    """
    Send message to log file as per settings in ini file.

    :param handle: (xclDeviceHandle) device handle
    :param level: (xrtLogMsgLevel) Severity level of the msg
    :param tag: (const char*) Tag supplied by the client, like "OCL", "XMA", etc.
    :param format: (const char *) Format of Msg string to write to log file
    :param ...: All other arguments as per the format
    :return: 0 on success or appropriate error number
    """
    libcore.xclAllocBO.restype = ctypes.c_int
    libcore.xclAllocBO.argtypes = [xclDeviceHandle, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
    return _valueOrError(libcore.xclLogMsg(handle, level, tag, format, *args))


def xclAllocBO(handle, size, unused, flags):
    """
    Allocate a BO of requested size with appropriate flags

    :param handle: (xclDeviceHandle) device handle
    :param size: (size_t) Size of buffer
    :param unused: (int) unused parameter present for legacy reasons
    :param flags: (unsigned int) Specify bank information, etc
    :return: BO handle
    """
    libcore.xclAllocBO.restype = ctypes.c_uint
    libcore.xclAllocBO.argtypes = [xclDeviceHandle, ctypes.c_size_t, ctypes.c_int, ctypes.c_uint]
    return _valueOrError(libcore.xclAllocBO(handle, size, unused, flags))


def xclAllocUserPtrBO(handle, userptr, size, flags):
    """
    Allocate a BO using userptr provided by the user
    :param handle: Device handle
    :param userptr: Pointer to 4K aligned user memory
    :param size: Size of buffer
    :param flags: Specify bank information, etc
    :return: BO handle
    """
    libcore.xclAllocUserPtrBO.restype = ctypes.c_uint
    libcore.xclAllocUserPtrBO.argtypes = [xclDeviceHandle, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint]
    return _valueOrError(libcore.xclAllocUserPtrBO(handle, userptr, size, flags))


def xclFreeBO(handle, boHandle):
    """
    Free a previously allocated BO

    :param handle: device handle
    :param boHandle: BO handle
    """
    libcore.xclFreeBO.restype = None
    libcore.xclFreeBO.argtypes = [xclDeviceHandle, ctypes.c_uint]
    libcore.xclFreeBO(handle, boHandle)


def xclWriteBO(handle, boHandle, src, size, seek):
    """
    Copy-in user data to host backing storage of BO
    :param handle: Device handle
    :param boHandle: BO handle
    :param src: Source data pointer
    :param size: Size of data to copy
    :param seek: Offset within the BO
    :return: 0 on success or appropriate error number
    """
    libcore.xclWriteBO.restype = ctypes.c_int
    libcore.xclWriteBO.argtypes = [xclDeviceHandle, ctypes.c_uint, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t]
    return _valueOrError(libcore.xclWriteBO(handle, boHandle, src, size, seek))


def xclReadBO(handle, boHandle, dst, size, skip):
    """
    Copy-out user data from host backing storage of BO
    :param handle: Device handle
    :param boHandle: BO handle
    :param dst: Destination data pointer
    :param size: Size of data to copy
    :param skip: Offset within the BO
    :return: 0 on success or appropriate error number
    """
    libcore.xclReadBO.restype = ctypes.c_int
    libcore.xclReadBO.argtypes = [xclDeviceHandle, ctypes.c_uint, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t]
    return _valueOrError(libcore.xclReadBO(handle, boHandle, dst, size, skip))


def xclMapBO(handle, boHandle, write, buf_type='char', buf_size=1):
    """
    Memory map BO into user's address space

    :param handle: (xclDeviceHandle) device handle
    :param boHandle: (unsigned int) BO handle
    :param write: (boolean) READ only or READ/WRITE mapping
    :param buf_type: type of memory mapped buffer
    :param buf_size: size of buffer
    :return: (pointer) Memory mapped buffer

    Map the contents of the buffer object into host memory
    To unmap the buffer call xclUnmapBO()

    Return type void pointer doesn't get correctly binded in ctypes
    To map the buffer, explicitly specify the type and size of data
    """
    prop = xclBOProperties()
    xclGetBOProperties(handle, boHandle, prop)

    if buf_type == 'char':
        libcore.xclMapBO.restype = ctypes.POINTER(ctypes.c_char * prop.size)
    elif buf_type == 'int':
        element_size = ctypes.sizeof(ctypes.c_int)
        size = prop.size/element_size
        libcore.xclMapBO.restype = ctypes.POINTER(ctypes.c_int * size)
    else:
        print("ERROR: This data type is not supported ")

    libcore.xclMapBO.argtypes = [xclDeviceHandle, ctypes.c_uint, ctypes.c_bool]
    ptr = libcore.xclMapBO(handle, boHandle, write)
    return ptr

def xclUnmapBO(handle, boHandle, addr):
    """
    Unmap a previously mapped BO from user's address space

    :param handle: (xclDeviceHandle) device handle
    :param boHandle: (unsigned int) BO handle
    :param addr: (pointer) buffer pointer

    """
    libcore.xclUnmapBO.restype = ctypes.c_int
    libcore.xclUnmapBO.argtypes = [xclDeviceHandle, ctypes.c_uint, ctypes.c_void_p]
    return _valueOrError(libcore.xclUnmapBO(handle, boHandle, addr))


def xclSyncBO(handle, boHandle, direction, size, offset):
    """
    Synchronize buffer contents in requested direction

    :param handle: (xclDeviceHandle) device handle
    :param boHandle: (unsigned int) BO handle
    :param direction: (xclBOSyncDirection) To device or from device
    :param size: (size_t) Size of data to synchronize
    :param offset: (size_t) Offset within the BO
    :return: 0 on success or standard errno
    """
    libcore.xclSyncBO.restype = ctypes.c_int
    libcore.xclSyncBO.argtypes = [xclDeviceHandle, ctypes.c_uint, ctypes.c_int, ctypes.c_size_t, ctypes.c_size_t]
    return _valueOrError(libcore.xclSyncBO(handle, boHandle, direction, size, offset))


def xclCopyBO(handle, dstBoHandle, srcBoHandle, size, dst_offset, src_offset):
    """
    Copy device buffer contents to another buffer
    :param handle: Device handle
    :param dstBoHandle: Destination BO handle
    :param srcBoHandle: Source BO handle
    :param size: Size of data to synchronize
    :param dst_offset: dst  Offset within the BO
    :param src_offset: src  Offset within the BO
    :return: 0 on success or standard errno
    """
    libcore.xclCopyBO.restype = ctypes.c_int
    libcore.xclCopyBO.argtypes = [xclDeviceHandle, ctypes.c_uint, ctypes.c_uint, ctypes.c_size_t, ctypes.c_size_t,
                               ctypes.c_uint]
    return _valueOrError(xclCopyBO(handle, dstBoHandle, srcBoHandle, size, dst_offset, src_offset))


def xclExportBO(handle, boHandle):
    """
    Obtain DMA-BUF file descriptor for a BO
    :param handle: Device handle
    :param boHandle: BO handle which needs to be exported
    :return: File handle to the BO or standard errno
    """
    libcore.xclExportBO.restype = ctypes.c_int
    libcore.xclExportBO.argtypes = [xclDeviceHandle, ctypes.c_uint]
    return _valueOrError(libcore.xclExportBO(handle, boHandle))


def xclImportBO(handle, fd, flags):
    """
    Obtain BO handle for a BO represented by DMA-BUF file descriptor
    :param handle: Device handle
    :param fd: File handle to foreign BO owned by another device which needs to be imported
    :param flags: Unused
    :return: BO handle of the imported BO

    Import a BO exported by another device.
    This operation is backed by Linux DMA-BUF framework
    """
    libcore.xclImportBO.restype = ctypes.c_int
    libcore.xclImportBO.argtypes = [xclDeviceHandle, ctypes.c_int, ctypes.c_uint]
    libcore.xclImportBO(handle, fd, flags)

def xclGetBOProperties(handle, boHandle, properties):
    """
    Obtain xclBOProperties struct for a BO

    :param handle: (xclDeviceHandle) device handle
    :param boHandle: (unsigned int) BO handle
    :param properties: BO properties struct pointer
    :return: 0 on success
    """
    libcore.xclGetBOProperties.restype = ctypes.c_int
    libcore.xclGetBOProperties.argtypes = [xclDeviceHandle, ctypes.c_uint, ctypes.POINTER(xclBOProperties)]
    return _valueOrError(libcore.xclGetBOProperties(handle, boHandle, properties))


def xclUnmgdPread(handle, flags, buf, size, offeset):
    """
    Perform unmanaged device memory read operation
    :param handle: Device handle
    :param flags: Unused
    :param buf: Destination data pointer
    :param size: Size of data to copy
    :param offeset: Absolute offset inside device
    :return: size of bytes read or appropriate error number

    This API may be used to perform DMA operation from absolute location specified. Users
    may use this if they want to perform their own device memory management -- not using the buffer
    object (BO) framework defined before.
    """
    libcore.xclUnmgdPread.restype = ctypes.c_size_t
    libcore.xclUnmgdPread.argtypes = [xclDeviceHandle, ctypes.c_uint, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint64]
    return libcore.xclUnmgdPread(handle, flags, buf, size, offeset)

def xclUnmgdPwrite(handle, flags, buf, size, offset):
    """
    Perform unmanaged device memory write operation
    :param handle: Device handle
    :param flags: Unused
    :param buf: Destination data pointer
    :param size: Size of data to copy
    :param offeset: Absolute offset inside device
    :return: size of bytes read or appropriate error number

    This API may be used to perform DMA operation from absolute location specified. Users
    may use this if they want to perform their own device memory management -- not using the buffer
    object (BO) framework defined before.
    """
    libcore.xclUnmgdPwrite.restype = ctypes.c_size_t
    libcore.xclUnmgdPwrite.argtypes = [xclDeviceHandle, ctypes.c_uint, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint64]
    return libcore.xclUnmgdPwrite(handle, flags, buf, size, offset)

def xclWrite(handle, space, offset, hostBuf, size):
    """
    Perform register write operation
    :param handle:  Device handle
    :param space: Address space
    :param offset: Offset in the address space
    :param hostBuf: Source data pointer
    :param size: Size of data to copy
    :return: size of bytes written or appropriate error number

    This API may be used to write to device registers exposed on PCIe BAR. Offset is relative to the
    the address space. A device may have many address spaces.
    This API will be deprecated in future. Please use this API only for IP bringup/debugging. For
    execution management please use XRT Compute Unit Execution Management APIs defined below
    """
    libcore.xclWrite.restype = ctypes.c_size_t
    libcore.xclWrite.argtypes = [xclDeviceHandle, ctypes.c_int, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_size_t]
    return libcore.xclWrite(handle, space, offset, hostBuf, size)

def xclRead(handle, space, offset, hostBuf, size):
    """
    Perform register write operation
    :param handle:  Device handle
    :param space: Address space
    :param offset: Offset in the address space
    :param hostBuf: Destination data pointer
    :param size: Size of data to copy
    :return: size of bytes written or appropriate error number

    This API may be used to write to device registers exposed on PCIe BAR. Offset is relative to the
    the address space. A device may have many address spaces.
    This API will be deprecated in future. Please use this API only for IP bringup/debugging. For
    execution management please use XRT Compute Unit Execution Management APIs defined below
    """
    libcore.xclRead.restype = ctypes.c_size_t
    libcore.xclRead.argtypes = [xclDeviceHandle, ctypes.c_int, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_size_t]
    return libcore.xclRead(handle, space, offset, hostBuf, size)

def xclExecBuf(handle, cmdBO):
    """
    xclExecBuf() - Submit an execution request to the embedded (or software) scheduler
    :param handle: Device handle
    :param cmdBO: BO handle containing command packet
    :return: 0 or standard error number

    Submit an exec buffer for execution. The exec buffer layout is defined by struct ert_packet
    which is defined in file *ert.h*. The BO should been allocated with DRM_XOCL_BO_EXECBUF flag.
    """
    libcore.xclExecBuf.restype = ctypes.c_int
    libcore.xclExecBuf.argtypes = [xclDeviceHandle, ctypes.c_uint]
    return _valueOrError(libcore.xclExecBuf(handle, cmdBO))

def xclExecBufWithWaitList(handle, cmdBO, num_bo_in_wait_list, bo_wait_list):
    """
    Submit an execution request to the embedded (or software) scheduler
    :param handle: Device handle
    :param cmdBO:BO handle containing command packet
    :param num_bo_in_wait_list: Number of BO handles in wait list
    :param bo_wait_list: BO handles that must complete execution before cmdBO is started
    :return:0 or standard error number

    Submit an exec buffer for execution. The BO handles in the wait
    list must complete execution before cmdBO is started.  The BO
    handles in the wait list must have beeen submitted prior to this
    call to xclExecBufWithWaitList.
    """
    libcore.xclExecBufWithWaitList.restype = ctypes.c_int
    libcore.xclExecBufWithWaitList.argtypes = [xclDeviceHandle, ctypes.c_uint, ctypes.c_size_t, ctypes.POINTER(ctypes.c_uint)]
    return _valueOrError(libcore.xclExecBufWithWaitList(handle, cmdBO, num_bo_in_wait_list, bo_wait_list))

def xclExecWait(handle, timeoutMilliSec):
    """
    xclExecWait() - Wait for one or more execution events on the device
    :param handle: Device handle
    :param timeoutMilliSec: How long to wait for
    :return:  Same code as poll system call

    Wait for notification from the hardware. The function essentially calls "poll" system
    call on the driver file handle. The return value has same semantics as poll system call.
    If return value is > 0 caller should check the status of submitted exec buffers
    """
    libcore.xclExecWait.restype = ctypes.c_int
    libcore.xclExecWait.argtypes = [xclDeviceHandle, ctypes.c_int]
    return libcore.xclExecWait(handle, timeoutMilliSec)

def xclRegisterInterruptNotify(handle, userInterrupt, fd):
    """
    register *eventfdfile handle for a MSIX interrupt
    :param handle: Device handle
    :param userInterrupt: MSIX interrupt number
    :param fd: Eventfd handle
    :return: 0 on success or standard errno

    Support for non managed interrupts (interrupts from custom IPs). fd should be obtained from
    eventfd system call. Caller should use standard poll/read eventfd framework in order to wait for
    interrupts. The handles are automatically unregistered on process exit.
    """
    libcore.xclRegisterInterruptNotify.restype = ctypes.c_int
    libcore.xclRegisterInterruptNotify.argtypes = [xclDeviceHandle, ctypes.c_uint, ctypes.c_int]
    return _valueOrError(libcore.xclRegisterInterruptNotify(handle, userInterrupt, fd))

class xclStreamContextFlags:
    XRT_QUEUE_FLAG_POLLING = (1 << 2)

class xclQueueContext(ctypes.Structure):
    # structure to describe a Queue
    _fields_ = [
     ("type", ctypes.c_uint32),
     ("state", ctypes.c_uint32),
     ("route", ctypes.c_uint64),
     ("flow", ctypes.c_uint64),
     ("qsize", ctypes.c_uint32),
     ("desc_size", ctypes.c_uint32),
     ("flags", ctypes.c_uint64)
    ]

def xclCreateWriteQueue(handle, q_ctx, q_hdl):
    """
    Create Write Queue
    :param handle:Device handle
    :param q_ctx:Queue Context
    :param q_hdl:Queue handle
    :return:

    This is used to create queue based on information provided in Queue context. Queue handle is generated if creation
    successes.
    This feature will be enabled in a future release.
    """
    libcore.xclCreateWriteQueue.restype = ctypes.c_int
    libcore.xclCreateWriteQueue.argtypes = [xclDeviceHandle, ctypes.POINTER(xclQueueContext), ctypes.c_uint64]
    return libcore.xclCreateWriteQueue(handle, q_ctx, q_hdl)

def xclCreateReadQueue(handle, q_ctx, q_hdl):
    """
    Create Read Queue
    :param handle:Device handle
    :param q_ctx:Queue Context
    :param q_hdl:Queue handle
    :return:

    This is used to create queue based on information provided in Queue context. Queue handle is generated if creation
    successes.
    This feature will be enabled in a future release.
    """
    libcore.xclCreateReadQueue.restype = ctypes.c_int
    libcore.xclCreateReadQueue.argtypes = [xclDeviceHandle, ctypes.POINTER(xclQueueContext), ctypes.c_uint64]
    return libcore.xclCreateReadQueue(handle, q_ctx, q_hdl)


def xclAllocQDMABuf(handle, size, buf_hdl):
    """
    Allocate DMA buffer
    :param handle: Device handle
    :param size: Buffer handle
    :param buf_hdl: Buffer size
    :return: buffer pointer

    These functions allocate and free DMA buffers which is used for queue read and write.
    This feature will be enabled in a future release.
    """
    libcore.xclAllocQDMABuf.restypes = ctypes.c_void_p
    libcore.xclAllocQDMABuf.argtypes = [xclDeviceHandle, ctypes.c_size_t, ctypes.c_uint64]
    return libcore.xclAllocQDMABuf(handle, size, buf_hdl)

def xclFreeQDMABuf(handle, buf_hdl):
    """
    Allocate DMA buffer
    :param handle: Device handle
    :param size: Buffer handle
    :param buf_hdl: Buffer size
    :return: buffer pointer

    These functions allocate and free DMA buffers which is used for queue read and write.
    This feature will be enabled in a future release.
    """
    libcore.xclFreeQDMABuf.restypes = ctypes.c_int
    libcore.xclFreeQDMABuf.argtypes = [xclDeviceHandle, ctypes.c_uint64]
    return libcore.xclFreeQDMABuf(handle, buf_hdl)

def xclDestroyQueue(handle, q_hdl):
    """
    Destroy Queue
    :param handle: Device handle
    :param q_hdl: Queue handle

    This function destroy Queue and release all resources. It returns -EBUSY if Queue is in running state.
    This feature will be enabled in a future release.
    """
    libcore.xclDestroyQueue.restypes = ctypes.c_int
    libcore.xclDestroyQueue.argtypes = [xclDeviceHandle, ctypes.c_uint64]
    return libcore.xclDestroyQueue(handle, q_hdl)

def xclModifyQueue(handle, q_hdl):
    """
    Modify Queue
    :param handle: Device handle
    :param q_hdl: Queue handle

    This function modifies Queue context on the fly. Modifying rid implies
    to program hardware traffic manager to connect Queue to the kernel pipe.
    """
    libcore.xclModifyQueue.restypes = ctypes.c_int
    libcore.xclModifyQueue.argtypes = [xclDeviceHandle, ctypes.c_uint64]
    return libcore.xclModifyQueue(handle, q_hdl)

def xclStartQueue(handle, q_hdl):
    """
    set Queue to running state
    :param handle: Device handle
    :param q_hdl: Queue handle

    This function set xclStartQueue to running state. xclStartQueue starts to process Read and Write requests.
    """
    libcore.xclStartQueue.restypes = ctypes.c_int
    libcore.xclStartQueue.argtypes = [xclDeviceHandle, ctypes.c_uint64]
    return libcore.xclStartQueue(handle, q_hdl)

def xclStopQueue(handle, q_hdl):
    """
    set Queue to init state
    :param handle: Device handle
    :param q_hdl: Queue handle

    This function set Queue to init state. all pending read and write requests will be flushed.
    wr_complete and rd_complete will be called with error wbe for flushed requests.
    """
    libcore.xclStopQueue.restypes = ctypes.c_int
    libcore.xclStopQueue.argtypes = [xclDeviceHandle, ctypes.c_uint64]
    return libcore.xclStopQueue(handle, q_hdl)

class anonymous_union(ctypes.Union):
    _fields_ = [
        ("buf", ctypes.POINTER(ctypes.c_char)),
        ("va", ctypes.c_uint64)
    ]

class xclReqBuffer(ctypes.Structure):
    _fields_ = [
        ("anonymous_union", anonymous_union),
        ("len", ctypes.c_uint64),
        ("buf_hdl", ctypes.c_uint64),
    ]

class xclQueueRequestKind:
    XCL_QUEUE_WRITE = 0
    XCL_QUEUE_READ  = 1

class xclQueueRequestFlag:
    XCL_QUEUE_REQ_EOT         = 1 << 0
    XCL_QUEUE_REQ_CDH         = 1 << 1
    XCL_QUEUE_REQ_NONBLOCKING = 1 << 2
    XCL_QUEUE_REQ_SILENT      = 1 << 3

class xclQueueRequest(ctypes.Structure):
    _fields_ = [
        ("op_code", ctypes.c_int),
        ("bufs", ctypes.POINTER(xclReqBuffer)),
        ("buf_num", ctypes.c_uint32),
        ("cdh", ctypes.POINTER(ctypes.c_char)),
        ("cdh_len", ctypes.c_uint32),
        ("flag", ctypes.c_uint32),
        ("priv_data", ctypes.c_void_p),
        ("timeout", ctypes.c_uint32)
    ]

class xclReqCompletion(ctypes.Structure):
    _fields_ = [
        ("resv", ctypes.c_char*64),
        ("priv_data", ctypes.c_void_p),
        ("nbytes", ctypes.c_size_t),
        ("err_code", ctypes.c_int)
    ]

def xclWriteQueue(handle, q_hdl, wr_req):
    """
    write data to queue
    :param handle: Device handle
    :param q_hdl: Queue handle
    :param wr_req: write request
    :return:

     This function moves data from host memory. Based on the Queue type, data is written as stream or packet.
     Return: number of bytes been written or error code.
         stream Queue:
             There is not any Flag been added to mark the end of buffer.
             The bytes been written should equal to bytes been requested unless error happens.
         Packet Queue:
             There is Flag been added for end of buffer. Thus kernel may recognize that a packet is receviced.
     This function supports blocking and non-blocking write
         blocking:
             return only when the entire buf has been written, or error.
         non-blocking:
             return 0 immediatly.
         EOT:
             end of transmit signal will be added at last
         silent: (only used with non-blocking);
             No event generated after write completes
    """
    libcore.xclWriteQueue.restype = ctypes.c_ssize_t
    libcore.xclWriteQueue.argtypes = [xclDeviceHandle, ctypes.POINTER(xclQueueRequest)]
    return libcore.xclWriteQueue(handle, q_hdl, wr_req)

def xclReadQueue(handle, q_hdl, wr_req):
    """
    write data to queue
    :param handle: Device handle
    :param q_hdl: Queue handle
    :param wr_req: write request
    :return:

     This function moves data to host memory. Based on the Queue type, data is read as stream or packet.
     Return: number of bytes been read or error code.
         stream Queue:
             read until all the requested bytes is read or error happens.
         blocking:
             return only when the requested bytes are read (stream) or the entire packet is read (packet)
         non-blocking:
             return 0 immidiately.
    """
    libcore.xclReadQueue.restype = ctypes.c_ssize_t
    libcore.xclReadQueue.argtypes = [xclDeviceHandle, ctypes.POINTER(xclQueueRequest)]
    return libcore.xclReadQueue(handle, q_hdl, wr_req)

def xclPollCompletion(handle, min_compl, max_compl, comps, actual_compl, timeout):
    """
    for non-blocking read/write, check if there is any request been completed
    :param handle: device handle
    :param min_compl: unblock only when receiving min_compl completions
    :param max_compl: Max number of completion with one poll
    :param comps:
    :param actual_compl:
    :param timeout: timeout
    :return:
    """
    libcore.xclPollCompletion.restype = ctypes.c_int
    libcore.xclPollCompletion.argtypes = [xclDeviceHandle, ctypes.c_int, ctypes.c_int, ctypes.POINTER(xclReqCompletion),
                                       ctypes.POINTER(ctypes.c_int), ctypes.c_int]
    return libcore.xclPollCompletion(handle, min_compl, max_compl, comps, actual_compl, timeout)

def xclRegRead(handle, cu_index, offset, datap):
    """
    Read register in register space of a CU
    :param handle: Device handle
    :param cu_index: CU index
    :param offset: Offset in the register space
    :param datap: Pointer to where result will be saved
    :return: 0 or appropriate error number
    """
    libcore.xclRegRead.restype = ctypes.c_int
    libcore.xclRegRead.argtypes = [xclDeviceHandle, ctypes.uint32_t, ctypes.uint32_t, ctypes.POINTER(ctypes.c_uint32_t)]
    return _valueOrError(libcore.xclRegRead(handle, cu_index, offset, datap))


def xclRegWrite(handle, cu_index, offset, data):
    """
    Write register in register space of a CU
    :param handle: Device handle
    :param cu_index: CU index
    :param offset: Offset in the register space
    :param data: Pointer to where result will be saved
    :return: 0 or appropriate error number
    """
    libcore.xclRegRead.restype = ctypes.c_int
    libcore.xclRegRead.argtypes = [xclDeviceHandle, ctypes.uint32_t, ctypes.uint32_t, ctypes.c_uint32_t]
    return _valueOrError(libcore.xclRegRead(handle, cu_index, offset, data))


def xclDebugReadIPStatus(handle, type, debugResults):
    """

    :param handle:
    :param type:
    :param debugResults:
    :return:
    """
    libcore.xclDebugReadIPStatus.restype = ctypes.c_size_t
    libcore.xclDebugReadIPStatus.argtypes = [xclDeviceHandle, ctypes.c_int, ctypes.c_void_p]
    return libcore.xclDebugReadIPStatus(handle, type, debugResults)

def xrtPLKernelOpen(handle, xclbinId, name):
    """
    Open a PL kernel and obtain its handle
    :param handle: Device handle
    :param xclbinId: UUID of the xclbin image running on the device
    :param name: Name of PL kernel
    :return: Kernel handle which must be closed with xrtKernelClose()
    """
    libcoreutil.xrtPLKernelOpen.restype = ctypes.POINTER(xrtKernelHandle)
    libcoreutil.xrtPLKernelOpen.argtypes = [xclDeviceHandle, ctypes.c_char_p, ctypes.c_char_p]
    return _valueOrError(libcoreutil.xrtPLKernelOpen(handle, xclbinId.bytes, name))


def xrtKernelClose(khandle):
    """
    Close an opened kernel
    :param khandle: Kernel handle obtained in xrtPLKernelOpen()
    :return: 0 or raises an OSError exception
    """
    libcoreutil.xrtKernelClose.restype = ctypes.c_int
    libcoreutil.xrtKernelClose.argtypes = [xrtKernelHandle]
    res = libcoreutil.xrtKernelClose(khandle)
    if (res):
        res = errno.EINVAL
    return _valueOrError(-res);


def xrtKernelRun(khandle, *args):
    """
    Start a kernel execution
    :param khandle: kernel handle obtained in xrtPLKernelOpen()
    :param args: variable number of kernel arguments
    :return: Run handle which must be closed with xrtRunClose()
    """
    libcoreutil.xrtKernelRun.restype = ctypes.POINTER(xrtKernelRunHandle)
    # TODO: Figure out how do we pass hint for tuple/varargs for ctypes
    # libcoreutil.xrtKerneRun.argtypes = [xrtKernelHandle]
    return libcoreutil.xrtKernelRun(khandle, *args)


def xrtRunWait(rhandle):
    """
    Wait for a kernel execution to finish
    :param rhandle: kernel run handle obtained in xrtKernelRun()
    :return: ert_cmd_state code
    """
    libcoreutil.xrtRunWait.restype = ctypes.c_int
    libcoreutil.xrtRunWait.argtypes = [xrtRunHandle]
    return libcoreutil.xrtRunWait(rhandle)


def xrtRunClose(rhandle):
    """
    Close a run handle
    :param rhandle: kernel run handle obtained in xrtKernelRun()
    :return: 0 or throw OSError with error code
    """
    libcoreutil.xrtRunClose.restype = ctypes.c_int
    libcoreutil.xrtRunClose.argtypes = [xrtRunHandle]
    res = libcoreutil.xrtRunClose(rhandle)
    if (res):
        res = errno.EINVAL
    return _valueOrError(-res);
